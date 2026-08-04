from pathlib import Path
from pydub import AudioSegment
from pydub.utils import which

# Explicitly set FFmpeg paths
FFMPEG = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"
FFPROBE = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffprobe.exe"

AudioSegment.converter = FFMPEG
AudioSegment.ffmpeg = FFMPEG
AudioSegment.ffprobe = FFPROBE


def merge_audio_segments(audio_folder: str, output_file: str):

    print("FFmpeg :", AudioSegment.converter)
    print("FFprobe:", AudioSegment.ffprobe)

    combined = AudioSegment.empty()

    audio_files = sorted(
        Path(audio_folder).glob("*.mp3"),
        key=lambda x: int(x.stem)
    )

    print(f"Found {len(audio_files)} audio files")

    for file in audio_files:
        print(f"Adding {file.name}")
        sound = AudioSegment.from_file(file, format="mp3")
        combined += sound

    combined.export(output_file, format="mp3")

    print("Merged successfully!")

    return output_file