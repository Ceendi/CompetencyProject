from sqlalchemy.orm import Session
from app.db.models import Job

def get_job(db: Session, job_id: int) -> Job | None:
    return db.query(Job).filter(Job.id == job_id).first()

def get_active_job_by_url(db: Session, url: str) -> Job | None:
    return db.query(Job).filter(Job.url == url, Job.status.in_(['pending', 'downloading', 'transcribing',
                                                                'analyzing'])).first()

def create_job(db: Session, url: str) -> Job:
    db_job = Job(url=url, status='pending')
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_status(db: Session, job_id: int, status: str):
    db_job = get_job(db, job_id)
    if db_job:
        db_job.status = status
        db.commit()

def set_job_complete(db: Session, job_id: int, film_id: int):
    db_job = get_job(db, job_id)
    if db_job:
        db_job.status = 'complete'
        db_job.film_id = film_id
        db.commit()

def set_job_failed(db: Session, job_id: int, error_message: str):
    db_job = get_job(db, job_id)
    if db_job:
        db_job.status = 'failed'
        db_job.error_message = error_message
        db.commit()
