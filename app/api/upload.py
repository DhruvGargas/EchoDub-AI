from fastapi import APIRouter, UploadFile, File, Form, Depends, BackgroundTasks
from app.services.processing_service import process_video
from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.job import Job

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    language: str = Form(...),
    db: Session = Depends(get_db),
):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = Job(
        filename=file.filename,
        language=language,
        status="uploaded"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(process_video, job.id)
    return {
    "job_id": job.id,
    "status": job.status,
    "message": "Video uploaded successfully. Processing started."
}