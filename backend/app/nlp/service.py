import asyncio
from app.nlp.engine import NlpEngine
from app.schemas.analysis import AnalysisBase


class SentimentService:
    def __init__(self, engine: NlpEngine):
        self.engine = engine

    async def analyze_sentiment(self, text: str) -> AnalysisBase:
        if not text:
            return AnalysisBase()

        raw_data = await asyncio.to_thread(self.engine.analyze_text_sync, text)

        return AnalysisBase(**raw_data)
