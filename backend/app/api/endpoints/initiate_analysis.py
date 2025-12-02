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
    active_job = crud_job.get_active_job_by_url(db, url=str(request.url))
    if active_job:
        return active_job

    existing_film = crud_film.get_film_by_url(db, url=str(request.url))
    if existing_film:
        new_job = crud_job.create_job(db, url=str(request.url))
        crud_job.set_job_complete(db, job_id=new_job.id, film_id=existing_film.id)
        db.refresh(new_job)
        return new_job

    new_job = crud_job.create_job(db, url=str(request.url))

    background_tasks.add_task(
        pipeline.run_full_pipeline,
        db=db,
        job_id=new_job.id
    )

    return new_job
