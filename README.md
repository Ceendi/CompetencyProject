# Video-Sent: Sentiment Analysis for Video Reviews

Video-Sent is a full-stack application that analyzes user sentiment from video reviews (e.g., YouTube). It downloads the video, transcribes the audio, performs sentiment analysis on various aspects (e.g., battery, screen, camera), and presents the results on a React-based dashboard.

## Features

- **Video Analysis**: Supports video links from YouTube.
- **Transcription**: Converts video audio to text.
- **Sentiment Analysis**: Aspect-based sentiment analysis of the transcribed text.
- **Dashboard**: Visualizes the analysis results.

## Architecture

The application is built with a modern full-stack architecture, separating the backend API from the frontend client.

### Backend

The backend is a Python-based RESTful API built with the following key technologies:

- **FastAPI**: A modern, high-performance web framework for building APIs.
- **SQLAlchemy**: The SQL toolkit and Object-Relational Mapper (ORM) for database interaction.
- **Alembic**: A lightweight database migration tool for SQLAlchemy.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **PostgreSQL**: The relational database for storing application data.

### Frontend

The frontend is a responsive single-page application (SPA) built with:

- **React**: A JavaScript library for building user interfaces.
- **Vite**: A next-generation frontend tooling that provides a faster and leaner development experience.
- **React Router**: For declarative routing within the application.
- **Framer Motion**: For creating fluid animations.

## Getting Started

### Prerequisites

- Docker and Docker Compose

- Node.js and npm (for local frontend development)

- Python 3.13+ and uv (for local backend development)

### Running with Docker (Recommended)

1.  **Create Environment File**:

    Copy the `.env.example` to a new file named `.env` and fill in the required values (e.g., `OPENAI_API_KEY`).

2.  **Build and Run**:

    ```bash

    docker-compose up --build

    ```

    The frontend will be available at `http://localhost:5173` and the backend at `http://localhost:8000`.

### Running Locally

#### Backend

1.  **Install Dependencies**:

    ```bash

    # Navigate to the backend directory

    cd backend

    # Install dependencies
    uv sync

    ```

2.  **Download NLP Models**:
    These models are required for sentiment analysis.

    ```bash
    # Navigate to the backend directory
    cd backend

    # Download SpaCy model
    python scripts/download_models.py --model_name pl_core_news_sm

    # Download Transformers model
    python scripts/download_models.py --model_name nlptown/bert-base-multilingual-uncased-sentiment
    ```

3.  **Run Migrations**:

    ```bash

    uv run alembic upgrade head

    ```

4.  **Start the Server**:

    ```bash

    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

    ```

#### Frontend

1.  **Install Dependencies**:

    ```bash
    # Navigate to the frontend directory
    cd frontend

    # Install dependencies
    npm install
    ```

2.  **Start the Development Server**:
    ```bash
    npm run dev
    ```

## Project Structure

```
.
├── backend
│   ├── app           # FastAPI application source
│   ├── alembic       # Database migrations
│   └── tests         # Backend tests
├── frontend
│   ├── src           # React application source
│   └── public        # Static assets
├── docker-compose.yml # Docker Compose configuration
└── .env.example      # Example environment variables
```

## API Endpoints

The backend API is available at `/api`. The main endpoints are:

- `POST /api/analysis/`: Initiate a new analysis for a video.
- `GET /api/status/{job_id}`: Get the status of an analysis job.
- `GET /api/result/{film_id}`: Get the final results of the analysis.

For more details, see the OpenAPI documentation at `http://localhost:8000/docs` when the backend is running.
