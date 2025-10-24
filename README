Project: Competency Project

## What this project is

This repository holds a full-stack app that analyzes phone reviews from short videos. The system accepts a link from YouTube, TikTok, or Instagram, downloads the video, transcribes the audio, and runs sentiment analysis on the text. The goal is to evaluate phone aspects such as specs, battery, screen, camera and return an aspect-level sentiment summary.

The full product has three main parts:

- Backend: Django REST API (in `backend/`)
- Frontend: React app (in `frontend/`) — user interface and forms to submit links
- Database: PostgreSQL

## Quick overview

- Language: Python (Django 5.x)
- Database: PostgreSQL
- Backend apps: `downloader`, `nlp_core`, `transcription`
- Frontend: React (in `frontend/` folder)
- Dashboard: client-side charts

## How it works (user flow)

1. User pastes a video link (YouTube / TikTok / Instagram) into the frontend form.
2. Frontend calls the backend API. The backend `downloader` app fetches and stores the video.
3. The `transcription` app extracts audio and creates a text transcript.
4. The `nlp_core` app performs aspect-based sentiment analysis (for phone specs, battery, screen, camera, etc.).
5. Results are stored in PostgreSQL and exposed via API endpoints.
6. The frontend dashboard visualizes the per-aspect sentiment (e.g., scores, counts, timelines).

## Run with Docker (recommended)

Prerequisites: Docker (Docker Compose)

1. Create a `.env` file in the repository root with these values (example):

```
DJANGO_SECRET_KEY=change-me
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_NAME=postgres
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
```

2. Build and start services with Docker Compose:

```bash
docker compose up --build
```

## Run locally without Docker (backend)

Prerequisites: Python 3.13+ (matching project's target)

Example commands for Windows PowerShell and Unix (bash):

PowerShell (Windows):

```powershell
# create virtualenv
python -m venv .venv
# activate
.\.venv\Scripts\Activate.ps1
# install
pip install --upgrade pip
pip install -r backend/requirements.txt
# run migrations
cd backend
python manage.py migrate
# run server
python manage.py runserver 0.0.0.0:8000
```

Bash (macOS / Linux):

```bash
# create virtualenv
python -m venv .venv
# activate
source .venv/bin/activate
# install
pip install --upgrade pip
pip install -r backend/requirements.txt
# run migrations
cd backend
python manage.py migrate
# run server
python manage.py runserver 0.0.0.0:8000
```

## Project structure (short)

- `backend/` — Django project (settings, apps, Dockerfile)
  - `core/` — project settings and URL config
  - `downloader/`, `nlp_core/`, `transcription/` — Django apps
- `frontend/` — React app (UI + dashboard)
- `docker-compose.yml` — Compose file to run Postgres + backend

## How to use (simple)

1. Start backend + db + frontend (Docker).
2. Open frontend in the browser, paste a video link and submit.
3. Wait for processing: the backend will download, transcribe and analyze. Results appear in the dashboard as charts and lists of aspect-level sentiments.

## Tests

Run tests using pytest in the Docker container:

```bash
docker-compose exec backend pytest
```

Or locally (if not using Docker):

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
cd backend
pytest

# Unix (bash)
source .venv/bin/activate
cd backend
pytest
```
