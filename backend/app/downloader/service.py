import asyncio
import logging
import os
import yt_dlp
from typing import Optional

logger = logging.getLogger(__name__)

AUDIO_OUTPUT_FOLDER = "/tmp/audio_downloads"
AUDIO_FORMAT = "mp3"


def _pobierz_audio_sync(url: str) -> Optional[str]:
    if not os.path.exists(AUDIO_OUTPUT_FOLDER):
        os.makedirs(AUDIO_OUTPUT_FOLDER)

    opcje = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': AUDIO_FORMAT,
            'preferredquality': '64',
        }],
        'outtmpl': os.path.join(AUDIO_OUTPUT_FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,

        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    try:
        with yt_dlp.YoutubeDL(opcje) as ydl:
            logger.info(f"Początek pobierania audio dla URL: {url}")

            info = ydl.extract_info(url, download=True)

            base_filename = ydl.prepare_filename(info)
            final_path = os.path.splitext(base_filename)[0] + f'.{AUDIO_FORMAT}'

            if os.path.exists(final_path):
                logger.info(f"Pomyślnie pobrano audio do: {final_path}")
                return final_path
            else:
                logger.error(f"Plik nie został znaleziony po pobraniu: {final_path}")
                return None

    except Exception as e:
        logger.error(f"Błąd pobierania audio dla {url}: {e}")
        return None


async def download_audio(url: str) -> str:
    audio_path = await asyncio.to_thread(_pobierz_audio_sync, url)

    if audio_path:
        return audio_path
    else:
        return "/tmp/download_error.mp3"