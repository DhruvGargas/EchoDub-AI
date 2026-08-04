# AI Video Dubbing API

A FastAPI backend for converting uploaded videos into dubbed versions using speech transcription, translation, text-to-speech, and FFmpeg-based audio replacement.

## Overview

This project provides an automated video dubbing pipeline that:

- receives uploaded videos through a `/upload` HTTP endpoint
- extracts audio from the video using FFmpeg
- transcribes speech with AssemblyAI
- translates transcript segments using the Gemini API
- generates dubbed speech with Microsoft Edge TTS voices
- adjusts generated audio timing to match the original speech segments
- merges the dubbed audio into the original video
- stores processing state in a SQL database

## Architecture

The backend is implemented in Python with:

- FastAPI for API endpoints and routing
- SQLAlchemy for job persistence
- AssemblyAI for speech-to-text transcription
- Gemini API for transcript translation
- edge-tts for text-to-speech generation
- FFmpeg for audio extraction, speed adjustment, concatenation, and final video audio replacement

Uploaded videos are saved to `uploads/`, and generated artifacts are written to `outputs/`.

## Required Configuration

Copy `.env.example` to `.env` and provide the following values:

- `DATABASE_URL` – SQLAlchemy database connection URL
- `ASSEMBLYAI_API_KEY` – API key for AssemblyAI transcription
- `GEMINI_API_KEY` – API key for Gemini translation

Note: `.env.example` also includes `HF_TOKEN`, but the current code path does not use it.

## Important Local Dependencies

The project expects FFmpeg binaries to be available at the hardcoded Windows path configured in these service files:

- `app/services/ffmpeg_service.py`
- `app/services/audio_speed_service.py`
- `app/services/audio_concat_service.py`
- `app/services/video_merge_service.py`

Update `FFMPEG_PATH` in those files if FFmpeg is installed elsewhere on your machine.

## Installation

Install Python dependencies from the repository root:

```powershell
pip install -r requirements.txt
```

## Running the API

Start the FastAPI application using Uvicorn:

```powershell
uvicorn app.main:app --reload
```

The API will start on `http://127.0.0.1:8000` by default.

## API Endpoints

### `POST /upload`

Upload a video and request a target language for dubbing.

Request form fields:

- `file`: video file upload
- `language`: target language for translation and TTS

Response contains the created job ID and processing status.

### `GET /jobs`

Retrieve a list of all uploaded jobs and their metadata.

### `GET /jobs/{job_id}`

Retrieve details for a single job.

### `GET /status/{job_id}`

Retrieve progress information for a job, including:

- `status`
- `current_step`
- `progress`
- `output_file`

### `GET /download/{job_id}`

Download the completed dubbed video once the job reaches `completed` status.

## Pipeline Behavior

The upload flow creates a `Job` record and runs `process_video` as a background task. The processing pipeline performs:

1. audio extraction from the uploaded video
2. transcription with AssemblyAI
3. translation of transcript segments via Gemini
4. speech generation using edge-tts
5. duration matching and speed adjustment for each dubbed segment
6. audio concatenation and mixing
7. audio replacement in the original video
8. database update with final job status and output file path

## Notes

- Created uploads and outputs are stored locally in `uploads/` and `outputs/`.
- The database engine is configured through `DATABASE_URL`.
- The current implementation assumes a Windows FFmpeg installation path; adjust the service files if running elsewhere.
- The project currently focuses on backend API behavior and does not include a frontend interface.
