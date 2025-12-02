import uvicorn
import logging
import os
import sys
from unittest.mock import patch

sys.path.append(os.getcwd())


async def mock_download_audio(*args, **kwargs):
    logging.info("MOCK: Simulating audio download")
    return {
        "path": "mock_audio.mp3",
        "title": "Mocked Video Title",
        "platform": "MockTube"
    }


async def mock_transcribe(*args, **kwargs):
    logging.info("MOCK: Simulating transcription")

    return "This is a sample text from mocked transcription in performance test."


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info(">>> STARTING SERVER WITH MOCKS (Performance Test) <<<")
    
    with patch("app.downloader.service.download_audio", side_effect=mock_download_audio), \
         patch("app.transcription.service.transcribe", side_effect=mock_transcribe):
        from app.main import app

        uvicorn.run(app, host="127.0.0.1", port=8000)
