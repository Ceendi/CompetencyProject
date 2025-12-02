import pytest
import asyncio
from unittest.mock import MagicMock, patch, mock_open
import os
from app.downloader.service import download_audio
from app.transcription.service import transcribe


@pytest.mark.asyncio
async def test_download_audio_success():
    test_url = "https://www.youtube.com/watch?v=test"

    import tempfile
    base_temp = os.path.join(tempfile.gettempdir(), "video_sent_audio_downloads")
    expected_path = os.path.join(base_temp, "Test Video.mp3")

    with patch("app.downloader.service.yt_dlp.YoutubeDL") as mock_ydl_cls:
        mock_instance = mock_ydl_cls.return_value
        mock_instance.__enter__.return_value = mock_instance
        mock_instance.__exit__.return_value = None

        mock_instance.extract_info.return_value = {
            "title": "Test Video",
            "extractor": "youtube",
            "ext": "mp3"
        }

        mock_instance.prepare_filename.return_value = os.path.join(base_temp, "Test Video.webm")

        with patch("app.downloader.service.os.makedirs") as mock_makedirs, \
                patch("app.downloader.service.os.path.exists") as mock_exists:
            mock_exists.return_value = True

            result = await download_audio(test_url)

            assert result is not None
            assert result["path"] == expected_path
            assert result["title"] == "Test Video"
            assert result["platform"] == "youtube"

            mock_instance.extract_info.assert_called_once_with(test_url, download=True)


@pytest.mark.asyncio
async def test_download_audio_failure():
    test_url = "https://www.youtube.com/watch?v=invalid"

    with patch("app.downloader.service.yt_dlp.YoutubeDL") as mock_ydl_cls:
        mock_instance = mock_ydl_cls.return_value
        mock_instance.__enter__.return_value = mock_instance

        mock_instance.extract_info.side_effect = Exception("Download failed")

        with patch("app.downloader.service.os.makedirs"):
            result = await download_audio(test_url)

            assert result is None


@pytest.mark.asyncio
async def test_transcribe_success():
    fake_path = "test_audio.mp3"
    fake_text = "This is a sample transcription."

    with patch("app.transcription.service.os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=b"audio_data")):
            with patch("app.transcription.service.aclient") as mock_client:
                mock_response = MagicMock()
                mock_response.text = fake_text

                mock_client.audio.transcriptions.create = MagicMock()
                future = asyncio.Future()
                future.set_result(mock_response)
                mock_client.audio.transcriptions.create.return_value = future

                result = await transcribe(fake_path)

                assert result == fake_text
                mock_client.audio.transcriptions.create.assert_called_once()


@pytest.mark.asyncio
async def test_transcribe_file_not_found():
    with patch("app.transcription.service.os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            await transcribe("non_existent_file.mp3")


@pytest.mark.asyncio
async def test_transcribe_api_error():
    with patch("app.transcription.service.os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=b"data")):
            with patch("app.transcription.service.aclient") as mock_client:
                mock_client.audio.transcriptions.create.side_effect = Exception("API Error")

                with pytest.raises(Exception, match="API Error"):
                    await transcribe("valid_file.mp3")
