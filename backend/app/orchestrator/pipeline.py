import logging
import os
from sqlalchemy.orm import Session

from app.downloader import service as downloader_service
from app.transcription import service as transcription_service
from app.nlp.service import SentimentService
from app.nlp.dependencies import get_engine

from app.crud import crud_job, crud_film, crud_analysis
from app.schemas import AnalysisCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_full_pipeline(db: Session, job_id: int):
    logger.info(f"[Job {job_id}]: Starting pipeline...")

    job = crud_job.get_job(db, job_id=job_id)
    if not job:
        logger.error(f"[Job {job_id}]: Job not found.")
        return

    audio_path = None

    try:
        # === DOWNLOADING ===
        crud_job.update_status(db, job_id=job_id, status="downloading")
        logger.info(f"[Job {job_id}]: Downloading audio from {job.url}...")

        download_result = await downloader_service.download_audio(url=job.url)
        
        if not download_result:
            raise Exception("Download failed.")

        audio_path = download_result["path"]
        title = download_result.get("title")
        platform = download_result.get("platform")
        
        logger.info(f"[Job {job_id}]: Download complete. File: {audio_path}")

        # === TRANSCRIPTION ===
        crud_job.update_status(db, job_id=job_id, status="transcribing")
        logger.info(f"[Job {job_id}]: Starting transcription...")

        transcribed_text = await transcription_service.transcribe(audio_path=audio_path)
        logger.info(f"[Job {job_id}]: Text: {transcribed_text[:50]}...")
        logger.info(f"[Job {job_id}]: Transcription complete.")

        # === NLP ANALYSIS ===
        crud_job.update_status(db, job_id=job_id, status="analyzing")
        logger.info(f"[Job {job_id}]: Starting sentiment analysis...")

        engine = get_engine()
        nlp_service_instance = SentimentService(engine=engine)

        sentiment_results = await nlp_service_instance.analyze_sentiment(text=transcribed_text)
        logger.info(f"Sentiment results: {sentiment_results}")
        logger.info(f"[Job {job_id}]: Sentiment analysis complete.")

        logger.info(f"[Job {job_id}]: Saving results to the database...")

        db_film = crud_film.create_film(
            db, 
            url=job.url,
            title=title,
            platform=platform,
            transcribed_text=transcribed_text
        )

        analysis_data = AnalysisCreate(**sentiment_results.model_dump())

        crud_analysis.create_analysis(db, analysis_data=analysis_data, film_id=db_film.id)

        crud_job.set_job_complete(db, job_id=job_id, film_id=db_film.id)
        logger.info(f"[Job {job_id}]: Pipeline finished successfully.")

    except Exception as e:
        error_msg = f"Pipeline error: {str(e)}"
        logger.error(f"[Job {job_id}]: {error_msg}", exc_info=True)

        crud_job.set_job_failed(db, job_id=job_id, error_message=error_msg)

    finally:
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                logger.info(f"[Job {job_id}]: Deleted temporary file {audio_path}")
            except Exception as cleanup_error:
                logger.warning(f"[Job {job_id}]: Failed to delete {audio_path}: {cleanup_error}")
