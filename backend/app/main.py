import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.nlp.engine import NlpEngine
from app.nlp.dependencies import set_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(">>> STARTUP: Initialazing Video-Sent API")

    nlp_engine = NlpEngine()
    try:
        nlp_engine.load_models()
        set_engine(nlp_engine)
    except Exception as e:
        logger.error(f"ERROR STARTING NLP: {e}")
        raise e

    yield

    logger.info(">>> SHUTDOWN: Closing app")
    set_engine(None)

app = FastAPI(
    title="Video-Sent API",
    description="API for sentiment analysis of video reviews.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
async def read_root():
    return {"status": "ok", "message": "Welcome to Video-Sent API!"}