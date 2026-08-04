import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

# Set API Key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Configure transcription
config = aai.TranscriptionConfig(
    speaker_labels=True
)

transcriber = aai.Transcriber()


def transcribe(audio_path: str):
    """
    Transcribes an audio file and returns:
    [
        {
            "speaker": "A",
            "start": 0.0,
            "end": 2.3,
            "text": "Hello everyone"
        }
    ]
    """

    transcript = transcriber.transcribe(audio_path, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"AssemblyAI Error: {transcript.error}")

    segments = []

    for utterance in transcript.utterances:
        segments.append(
            {
                "speaker": utterance.speaker,
                "start": utterance.start / 1000,
                "end": utterance.end / 1000,
                "text": utterance.text,
            }
        )

    return segments