from mutagen.mp3 import MP3


def get_audio_duration(audio_file: str) -> float:
    """
    Returns the duration of an MP3 file in seconds.
    """

    audio = MP3(audio_file)

    return audio.info.length