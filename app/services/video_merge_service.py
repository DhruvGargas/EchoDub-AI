import subprocess

FFMPEG_PATH = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"


def replace_audio(video_path, audio_path, output_path):

    subprocess.run(
        [
            FFMPEG_PATH,
            "-y",
            "-i", video_path,
            "-i", audio_path,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path,
        ],
        check=True,
    )

    return output_path