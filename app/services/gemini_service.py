import os
import json
import re

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Change this if needed
MODEL_NAME = "gemini-3.5-flash-lite"


def translate_transcript(transcript, target_language):
    """
    Translate transcript while preserving segment count.
    """

    transcript_json = json.dumps(
        [
            {
                "text": segment["text"]
            }
            for segment in transcript
        ],
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""
You are an expert audiovisual dubbing translator.

Translate the following English transcript into {target_language}.

Your translation will later be converted into speech.

Rules:

1. Preserve EXACT number of transcript segments.
2. Return EXACTLY {len(transcript)} JSON objects.
3. Return ONLY JSON.
4. No markdown.
5. No explanations.

Each object must be:

{{
  "translated": "..."
}}

Transcript:

{transcript_json}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    text = response.text.strip()

    print("\n========== GEMINI RESPONSE ==========")
    print(text)
    print("=====================================\n")

    text = re.sub(r"^```(?:json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    try:
        data = json.loads(text)

    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Gemini returned invalid JSON:\n{text}\n\n{e}"
        )

    if len(data) != len(transcript):
        raise RuntimeError(
            f"Expected {len(transcript)} segments, got {len(data)}."
        )

    cleaned = []

    for item in data:

        translated = item["translated"].strip()

        translated = re.sub(
            r"^\d+[\.\)]\s*",
            "",
            translated,
        )

        translated = re.sub(r"\s+", " ", translated)

        cleaned.append(
            {
                "translated": translated
            }
        )

    return cleaned