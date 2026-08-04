from sqlalchemy.orm import Session
from app.models.job import Job


def update_job_progress(
    db: Session,
    job: Job,
    step: str,
    progress: int,
    status: str = "processing",
):
    """
    Update the job's processing status, current step and progress.
    """

    job.status = status
    job.current_step = step
    job.progress = progress

    db.commit()
    db.refresh(job)