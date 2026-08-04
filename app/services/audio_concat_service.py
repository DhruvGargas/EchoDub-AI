import os
import subprocess

FFMPEG_PATH = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"


def concatenate_audio(audio_folder: str, translated_segments: list, output_file: str):
    """
    Place each generated speech clip at its original timestamp
    using FFmpeg adelay + amix.
    """

    inputs = []
    filter_parts = []

    for i, segment in enumerate(translated_segments):

        audio_file = os.path.join(audio_folder, f"{i}.mp3")

        if not os.path.exists(audio_file):
            raise FileNotFoundError(audio_file)

        inputs.extend(["-i", audio_file])

        delay_ms = int(segment["start"] * 1000)

        filter_parts.append(
            f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]"
        )

    mixed_inputs = "".join(f"[a{i}]" for i in range(len(translated_segments)))

    filter_complex = (
        ";".join(filter_parts)
        + ";"
        + f"{mixed_inputs}amix=inputs={len(translated_segments)}:normalize=0[out]"
    )

    command = [
        FFMPEG_PATH,
        "-y",
        *inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        "[out]",
        output_file,
    ]

    print("\n========== TIMELINE MIX ==========")
    print(filter_complex)
    print("==================================\n")

    subprocess.run(command, check=True)

    print(f"✓ Timeline audio created: {output_file}")

    return output_file