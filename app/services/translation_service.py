from app.services.gemini_service import translate_transcript


def translate_segments(transcript, target_language="Hindi"):

    if not transcript:
        return []

    translated = translate_transcript(
        transcript,
        target_language
    )

    result = []

    for original, translated_segment in zip(transcript, translated):

        result.append({
    "speaker": original.get("speaker"),
    "start": original["start"],
    "end": original["end"],
    "original": original["text"],
    "translated": translated_segment["translated"]
})

    return result