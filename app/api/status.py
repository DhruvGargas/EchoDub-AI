from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.job import Job

router = APIRouter(prefix="/status", tags=["Status"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{job_id}")
def get_job_status(job_id: int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "id": job.id,
        "status": job.status,
        "current_step": job.current_step,
        "progress": job.progress,
        "output_file": job.output_file,
    }