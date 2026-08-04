import subprocess
from pathlib import Path

FFMPEG_PATH = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"


def adjust_audio_speed(input_file: str, output_file: str, speed_factor: float):
    """
    Adjust the playback speed of an audio file using FFmpeg.
    """

    # FFmpeg's atempo supports values between 0.5 and 2.0
    speed_factor = max(0.5, min(2.0, speed_factor))

    command = [
        FFMPEG_PATH,
        "-y",
        "-i",
        input_file,
        "-filter:a",
        f"atempo={speed_factor:.4f}",
        output_file,
    ]

    subprocess.run(command, check=True)