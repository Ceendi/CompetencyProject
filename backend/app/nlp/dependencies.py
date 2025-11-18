from typing import Annotated
from fastapi import Depends, HTTPException
from app.nlp.engine import NlpEngine
from app.nlp.service import SentimentService

_engine_instance: NlpEngine | None = None

def set_engine(engine: NlpEngine) -> None:
    global _engine_instance
    _engine_instance = engine

def get_engine() -> NlpEngine:
    if _engine_instance is None:
        raise HTTPException(status_code=503, detail="NLP Engine not initialized")
    return _engine_instance

def get_nlp_service(
    engine: Annotated[NlpEngine, Depends(get_engine)]
) -> SentimentService:
    return SentimentService(engine)
