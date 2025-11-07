# Video-Sent: Sentiment Analysis for Video Reviews

Video-Sent is a full-stack application that analyzes user sentiment from video reviews (e.g., YouTube). It downloads the video, transcribes the audio, performs sentiment analysis on various aspects (e.g., battery, screen, camera), and presents the results on a React-based dashboard.

## Features

- **Video Analysis**: Supports video links from YouTube.
- **Transcription**: Converts video audio to text.
- **Sentiment Analysis**: Aspect-based sentiment analysis of the transcribed text.
- **Dashboard**: Visualizes the analysis results.

## Getting Started

### Prerequisites

- Docker and Docker Compose

- Node.js and npm (for local frontend development)

- Python 3.14+ and uv (for local backend development)

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

    uv pip sync

    ```

2.  **Run Migrations**:

    ```bash

    uv run alembic upgrade head

    ```

3.  **Start the Server**:

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
- `GET /api/analysis/{analysis_id}`: Get the status and results of an analysis.

For more details, see the OpenAPI documentation at `http://localhost:8000/docs` when the backend is running.
