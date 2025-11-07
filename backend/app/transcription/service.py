import asyncio
import logging
logger = logging.getLogger(__name__)

async def transcribe(audio_path: str) -> str:
    await asyncio.sleep(10)
    logger.info(f"Transcription complete for: {audio_path}")
    return "The battery is great, but the screen is weak."