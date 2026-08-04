import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.job import Job

router = APIRouter()


# ----------------------------------------
# Get all jobs
# ----------------------------------------
@router.get("/jobs")
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = (
        db.query(Job)
        .order_by(Job.created_at.desc())
        .all()
    )

    return [
        {
            "job_id": job.id,
            "filename": job.filename,
            "language": job.language,
            "status": job.status,
            "output_file": job.output_file,
            "created_at": job.created_at,
        }
        for job in jobs
    ]


# ----------------------------------------
# Get single job
# ----------------------------------------
@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return {
        "job_id": job.id,
        "filename": job.filename,
        "language": job.language,
        "status": job.status,
        "output_file": job.output_file,
        "created_at": job.created_at,
    }


# ----------------------------------------
# Delete job
# ----------------------------------------
@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Delete generated output file if it exists
    if job.output_file and os.path.exists(job.output_file):
        os.remove(job.output_file)

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully.",
        "job_id": job_id
    }