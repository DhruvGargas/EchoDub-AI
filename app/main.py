from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router
from app.db.database import engine
from app.models.job import Job
from app.api.jobs import router as jobs_router
from app.api.download import router as download_router
from app.api.status import router as status_router
Job.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Video Dubbing API",
    description="Backend API for multilingual video dubbing",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload_router)
app.include_router(jobs_router)
app.include_router(download_router)
app.include_router(status_router)
@app.get("/")
def root():
    return {
        "message": "Welcome to AI Video Dubbing API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }