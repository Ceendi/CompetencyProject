import logging
import spacy
import torch
from transformers import pipeline
from statistics import mean
from app.nlp.definitions import AspectCatalog
from app.core.config import settings

logger = logging.getLogger(__name__)


class NlpEngine:
    def __init__(self):
        self.nlp = None
        self.sentiment_pipeline = None
        self._is_loaded = False

    def load_models(self) -> None:
        if self._is_loaded:
            return

        logger.info(f"NLP Engine: Loading SpaCy model ({settings.NLP_SPACY_MODEL})...")
        try:
            self.nlp = spacy.load(settings.NLP_SPACY_MODEL)
        except OSError:
            logger.warning(f"Model '{settings.NLP_SPACY_MODEL} not found'. Using fallback (blank).")
            self.nlp = spacy.blank("pl" if "pl" in settings.NLP_SPACY_MODEL else "en")
            self.nlp.add_pipe("sentencizer")

        logger.info(f"NLP Engine: Loading Transformers ({settings.NLP_TRANSFORMER_MODEL})...")
        device = 0 if torch.cuda.is_available() else -1

        self.sentiment_pipeline = pipeline(
            task="text-classification",
            model=settings.NLP_TRANSFORMER_MODEL,
            device=device,
            truncation=True,
            max_length=512
        )

        self._is_loaded = True
        logger.info("NLP Engine: Ready.")

    def analyze_text_sync(self, text: str) -> dict[str, float | None]:
        if not self._is_loaded:
            raise RuntimeError("Models not loaded! Check lifecycle.")

        if not text:
            return {}

        import re
        clause_splitter = re.compile(r'\s+(?:ale|i|a|jednak|lecz)\s+', re.IGNORECASE)

        doc = self.nlp(text)
        scores: dict[str, list[float]] = {a.key: [] for a in AspectCatalog.ASPECTS}

        for sent in doc.sents:
            clauses = clause_splitter.split(sent.text)

            for clause in clauses:
                if not clause.strip():
                    continue

                clause_lower = clause.lower()

                active_aspects_in_clause = [
                    aspect.key
                    for aspect in AspectCatalog.ASPECTS
                    if any(kw in clause_lower for kw in aspect.keywords)
                ]

                if active_aspects_in_clause:
                    result = self.sentiment_pipeline(clause)[0]
                    normalized_score = self._normalize_stars(result['label'])

                    for key in active_aspects_in_clause:
                        scores[key].append(normalized_score)

        return {
            key: round(mean(val), 2) if val else None
            for key, val in scores.items()
        }

    @staticmethod
    def _normalize_stars(label: str) -> float:
        try:
            stars = int(label.split()[0])
            return (stars - 3) / 2.0
        except (ValueError, IndexError):
            return 0.0
