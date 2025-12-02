import pytest
from unittest.mock import MagicMock, patch
from app.nlp.engine import NlpEngine


@pytest.fixture
def mock_engine():
    with patch("app.nlp.engine.spacy.load") as mock_spacy_load, \
            patch("app.nlp.engine.pipeline") as mock_pipeline:
        engine = NlpEngine()

        mock_nlp = MagicMock()
        mock_spacy_load.return_value = mock_nlp

        mock_sentiment_pipeline = MagicMock()
        mock_pipeline.return_value = mock_sentiment_pipeline

        engine.load_models()

        engine.mock_nlp = mock_nlp
        engine.mock_pipeline = mock_sentiment_pipeline

        return engine


def test_analyze_text_logic(mock_engine):
    mock_doc = MagicMock()
    mock_sent1 = MagicMock()
    mock_sent1.text = "Battery is great."
    mock_sent2 = MagicMock()
    mock_sent2.text = "Screen is bad."

    mock_doc.sents = [mock_sent1, mock_sent2]
    mock_engine.mock_nlp.return_value = mock_doc

    mock_engine.mock_pipeline.side_effect = [
        [{"label": "5 stars", "score": 0.9}],
        [{"label": "1 star", "score": 0.9}]
    ]

    result = mock_engine.analyze_text_sync("Dummy text")

    assert result["battery"] == 1.0
    assert result["screen"] == -1.0
    assert result["price"] is None


def test_analyze_text_averaging(mock_engine):
    mock_doc = MagicMock()
    s1 = MagicMock()
    s1.text = "Battery ok."
    s2 = MagicMock()
    s2.text = "Battery great."

    mock_doc.sents = [s1, s2]
    mock_engine.mock_nlp.return_value = mock_doc

    mock_engine.mock_pipeline.side_effect = [
        [{"label": "3 stars", "score": 0.9}],
        [{"label": "5 stars", "score": 0.9}]
    ]

    result = mock_engine.analyze_text_sync("Dummy text")

    assert result["battery"] == 0.5
