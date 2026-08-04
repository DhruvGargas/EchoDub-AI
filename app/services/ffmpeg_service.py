import subprocess
from pathlib import Path

FFMPEG_PATH = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"


def extract_audio(video_path: str):
    output_audio = Path(video_path).with_suffix(".wav")

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(output_audio),
    ]

    subprocess.run(command, check=True)

    return str(output_audio)