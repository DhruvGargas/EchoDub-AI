import asyncio
import edge_tts

# Speaker-aware voices for each language
LANGUAGE_VOICES = {
    "English": {
        "A": "en-US-GuyNeural",
        "B": "en-US-JennyNeural",
        "C": "en-US-GuyNeural",
        "D": "en-US-JennyNeural",
    },

    "Hindi": {
        "A": "hi-IN-MadhurNeural",
        "B": "hi-IN-SwaraNeural",
        "C": "hi-IN-MadhurNeural",
        "D": "hi-IN-SwaraNeural",
    },

    "French": {
        "A": "fr-FR-HenriNeural",
        "B": "fr-FR-DeniseNeural",
    },

    "Spanish": {
        "A": "es-ES-AlvaroNeural",
        "B": "es-ES-ElviraNeural",
    },
}


def get_voice(language: str, speaker: str = None) -> str:
    """
    Returns the appropriate voice based on language and speaker.
    Falls back gracefully if the language or speaker is unknown.
    """

    language = language.strip()

    if language not in LANGUAGE_VOICES:
        return "en-US-JennyNeural"

    voices = LANGUAGE_VOICES[language]

    if speaker is None:
        return list(voices.values())[0]

    return voices.get(speaker, list(voices.values())[0])


async def generate_voice(
    text: str,
    output_file: str,
    language: str,
    speaker: str = None,
):
    voice = get_voice(language, speaker)

    print("\n" + "=" * 60)
    print("EDGE TTS DEBUG")
    print("=" * 60)
    print(f"Speaker : {speaker}")
    print(f"Language: {language}")
    print(f"Voice   : {voice}")
    print(f"Text    : {repr(text)}")
    print("=" * 60 + "\n")

    if not text or not text.strip():
        raise ValueError("Empty text received for TTS.")

    communicate = edge_tts.Communicate(
        text=text.strip(),
        voice=voice,
    )

    await communicate.save(output_file)

    print(f"✅ Audio saved successfully: {output_file}")


def text_to_speech(
    text: str,
    output_file: str,
    language: str,
    speaker: str = None,
):
    asyncio.run(
        generate_voice(
            text=text,
            output_file=output_file,
            language=language,
            speaker=speaker,
        )
    )