from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import film as film_schema
from app.schemas import job as job_schema
from app.crud import crud_film, crud_job
from app.orchestrator import pipeline

router = APIRouter()


@router.post(
    "/",
    response_model=job_schema.JobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def initiate_analysis_endpoint(
        background_tasks: BackgroundTasks,
        request: film_schema.FilmCreate,
        db: Session = Depends(get_db)
):
    existing_film = crud_film.get_film_by_url(db, url=str(request.url))
    if existing_film:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This URL has already been successfully analyzed."
        )

    # 2. Check if a job for this URL is already active (in progress)
    active_job = crud_job.get_active_job_by_url(db, url=str(request.url))
    if active_job:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Analysis for this URL is already in progress."
        )

    new_job = crud_job.create_job(db, url=str(request.url))

    background_tasks.add_task(
        pipeline.run_full_pipeline,
        db=db,
        job_id=new_job.id
    )

    return new_job
