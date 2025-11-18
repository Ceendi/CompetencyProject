from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import job as job_schema
from app.crud import crud_job

router = APIRouter()


@router.get(
    "/{job_id}",
    response_model=job_schema.JobStatusResponse
)
async def get_job_status_endpoint(
        job_id: int,
        db: Session = Depends(get_db)
):
    job = crud_job.get_job(db, job_id=job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job with the specified ID was not found."
        )

    return job
