from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    language = Column(String, nullable=False)

    # queued | processing | completed | failed
    status = Column(String, default="queued", nullable=False)

    # Current processing step
    current_step = Column(String, default="Queued", nullable=False)

    # Progress percentage (0–100)
    progress = Column(Integer, default=0, nullable=False)

    output_file = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )