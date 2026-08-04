import os
import json
import traceback

from app.db.database import SessionLocal
from app.models.job import Job
from app.services.job_status_service import update_job_progress
from app.services.ffmpeg_service import extract_audio
from app.services.assemblyai_service import transcribe
from app.services.translation_service import translate_segments
from app.services.tts_service import text_to_speech
from app.services.audio_concat_service import concatenate_audio
from app.services.video_merge_service import replace_audio

from app.services.audio_utils import get_audio_duration
from app.services.audio_speed_service import adjust_audio_speed


def process_video(job_id: int):

    db = SessionLocal()

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    job = None

    try:

        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            print(f"Job {job_id} not found.")
            return

        update_job_progress(
    db=db,
    job=job,
    step="Starting Pipeline",
    progress=5,
)

        print("\n========== AI PIPELINE START ==========\n")

        # -----------------------------------
        # STEP 1: Extract Audio
        # -----------------------------------

        video_path = os.path.join("uploads", job.filename)
        update_job_progress(
    db=db,
    job=job,
    step="Extracting Audio",
    progress=10,
)
        print("Extracting audio...")

        audio_path = extract_audio(video_path)

        print(f"✓ Audio extracted: {audio_path}")

        # -----------------------------------
        # STEP 2: Speech To Text
        # -----------------------------------
        update_job_progress(
    db=db,
    job=job,
    step="Transcribing Speech",
    progress=25,
)
        print("Transcribing audio...")

        transcript = transcribe(audio_path)

        transcript_path = f"outputs/{job.id}_transcript.json"

        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(transcript, f, indent=4, ensure_ascii=False)

        print(f"✓ Transcript saved: {transcript_path}")

        # -----------------------------------
        # STEP 3: Translation
        # -----------------------------------
        update_job_progress(
    db=db,
    job=job,
    step="Translating Transcript",
    progress=45,
)
        print("Translating transcript...")

        translated = translate_segments(
            transcript,
            target_language=job.language
        )

        translated_path = f"outputs/{job.id}_translated.json"

        with open(translated_path, "w", encoding="utf-8") as f:
            json.dump(translated, f, indent=4, ensure_ascii=False)

        print(f"✓ Translation saved: {translated_path}")

        # -----------------------------------
        # STEP 4: Text To Speech
        # -----------------------------------
        update_job_progress(
    db=db,
    job=job,
    step="Generating AI Voices",
    progress=65,
)
        print("Generating AI voice...")

        audio_folder = f"outputs/{job.id}_audio"

        os.makedirs(audio_folder, exist_ok=True)

        for i, segment in enumerate(translated):

            output_file = os.path.join(audio_folder, f"{i}.mp3")

            text_to_speech(
                text=segment["translated"],
                output_file=output_file,
                language=job.language,
                speaker=segment.get("speaker")
            )

            # -----------------------------------
            # Match TTS duration to original duration
            # -----------------------------------

            original_duration = segment["end"] - segment["start"]

            generated_duration = get_audio_duration(output_file)

            # Avoid division by zero
            if original_duration <= 0:
                print(f"Skipping speed adjustment for segment {i}")
                continue

            speed_factor = generated_duration / original_duration

            print("\n" + "=" * 60)
            print(f"SEGMENT {i}")
            print(f"Original Duration : {original_duration:.2f}s")
            print(f"Generated Duration: {generated_duration:.2f}s")
            print(f"Speed Factor      : {speed_factor:.2f}")
            print("=" * 60)

            adjusted_file = os.path.join(
                audio_folder,
                f"{i}_adjusted.mp3"
            )

            adjust_audio_speed(
                input_file=output_file,
                output_file=adjusted_file,
                speed_factor=speed_factor
            )

            os.remove(output_file)
            os.rename(adjusted_file, output_file)

        print("✓ All speech segments generated.")

        # -----------------------------------
        # STEP 5: Merge Audio Segments
        # -----------------------------------
        update_job_progress(
    db=db,
    job=job,
    step="Synchronizing Audio",
    progress=85,
)
        print("Merging audio segments...")

        final_audio = f"outputs/{job.id}_final_audio.mp3"

        concatenate_audio(
    audio_folder=audio_folder,
    translated_segments=translated,
    output_file=final_audio,
)

        print(f"✓ Final audio created: {final_audio}")

        # -----------------------------------
        # STEP 6: Replace Original Audio
        # -----------------------------------
        update_job_progress(
    db=db,
    job=job,
    step="Merging Audio with Video",
    progress=95,
)
        print("Creating dubbed video...")

        dubbed_video = f"outputs/{job.id}_dubbed_video.mp4"

        replace_audio(
            video_path,
            final_audio,
            dubbed_video
        )

        print(f"✓ Dubbed video created: {dubbed_video}")

        # -----------------------------------
        # STEP 7: Update Database
        # -----------------------------------

        job.status = "completed"
        job.current_step = "Completed"
        job.progress = 100
        job.output_file = dubbed_video

        db.commit()
        db.refresh(job)

        print("\n========== AI PIPELINE FINISHED ==========\n")

    except Exception:

        print("\n========== PIPELINE FAILED ==========\n")

        traceback.print_exc()

        if job:
            job.status = "failed"
            job.current_step = "Failed"
            job.progress = 0

            db.commit()
            db.refresh(job)

    finally:

        db.close()