from faster_whisper import WhisperModel

print("Loading Whisper model...")

model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)

print("Whisper model loaded.")

def transcribe(audio_path: str):
    print("Starting transcription...")

    segments, info = model.transcribe(
        audio_path,
        language="en",
        beam_size=5
    )

    print("Transcription finished.")

    transcript = []

    for segment in segments:
        print(segment.text)

        transcript.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return transcript