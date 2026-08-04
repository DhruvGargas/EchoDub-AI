from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.db.dependencies import get_db
from app.models.job import Job

router = APIRouter(prefix="/download", tags=["Download"])


@router.get("/{job_id}")
def download_video(job_id: int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Video is still processing."
        )

    if not job.output_file:
        raise HTTPException(
            status_code=404,
            detail="Output file not found."
        )

    if not os.path.exists(job.output_file):
        raise HTTPException(
            status_code=404,
            detail="File does not exist on disk."
        )

    return FileResponse(
        path=job.output_file,
        media_type="video/mp4",
        filename=os.path.basename(job.output_file)
    )