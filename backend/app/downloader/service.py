import asyncio
import logging
logger = logging.getLogger(__name__)

async def download_audio(url: str) -> str:
    await asyncio.sleep(5)
    logger.info(f"Downloaded audio for: {url}")
    return "/tmp/audio_file.mp3"