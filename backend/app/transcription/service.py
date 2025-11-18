import os
import logging
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def transcribe(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        logger.error(f"File not found: {audio_path}")
        return "Error: File not found"

    try:
        logger.info(f"Starting OpenAI transcription for: {audio_path}")

        with open(audio_path, "rb") as audio_file:
            transcript = await aclient.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        text = transcript.text
        logger.info(f"Transcription complete for: {audio_path}")
        return text

    except Exception as e:
        logger.error(f"OpenAI Error: {e}")
        return f"BŁĄD OpenAI: {e}"