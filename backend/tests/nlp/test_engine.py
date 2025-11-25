import pytest
from app.nlp.engine import NlpEngine
from app.core import config

TEST_TEXT = """Ależ to będzie hit! Szanowni Państwo, przed Wami iPhone 17, czyli bazowy model, od którego nie oczekiwało się zbyt wiele, a okazuje się, że dostaniemy bardzo dużo. A przynajmniej jak na Apple'a, bo rzecz jasna konkurencja daje nam to od lat. Po pierwsze, ekran urósł, zamiast 6,1 mamy 6,3 cala. Po drugie, jasność jest taka sama, szczytowa, jak w modelach Pro. Mamy ekran adaptacyjny od 1 do 120 Hz, zatem mamy także pełnoprawne Always On Display od Apple'a. No i po czwarte, mamy dodatkowo pamięć nie 128, a 256 GB, zachowując dokładnie tę samą cenę. Czyli od 3999 zł. A biorąc pod uwagę konkurencję w postaci Samsunga Galaxy S25 bazowego, czy Pixela 10, które cenowo podczas premiery stały bardzo podobnie, uważam, że iPhone 17 nie ma się czego wstydzić i może się okazać jednym z największych hitów tego i przyszłego roku, jeżeli chodzi o sprzedaż. Recenzja wkrótce."""

@pytest.fixture(scope="module")
def nlp_engine():
    config.settings.NLP_SPACY_MODEL = "pl_core_news_sm"
    config.settings.NLP_TRANSFORMER_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
    
    engine = NlpEngine()
    engine.load_models()
    return engine

def test_nlp_analysis_iphone_review(nlp_engine):
    result = nlp_engine.analyze_text_sync(TEST_TEXT)

    assert result["screen"] == 0.33
    assert result["memory"] == 0.0
    assert result["price"] == 0.0

    assert result["quick_charge"] is None

    assert result["battery"] is None
    assert result["camera"] is None
    assert result["audio"] is None


def test_nlp_analysis_negative_review(nlp_engine):
    text = "Ten telefon to totalna porażka. Bateria trzyma ledwo 2 godziny, to jakiś żart. Ekran jest ciemny, nic nie widać w słońcu. Aparat robi rozmazane zdjęcia, jakość jest fatalna. A cena? 5000 zł za taki złom to kradzież. Nie polecam nikomu!"
    
    result = nlp_engine.analyze_text_sync(text)

    assert result["battery"] <= -0.5
    assert result["screen"] <= -0.5
    assert result["camera"] <= -0.5
    assert result["price"] <= -0.5


def test_nlp_analysis_positive_review(nlp_engine):
    text = "Bateria jest rewelacyjna. Ekran to mistrzostwo świata. Aparat jest perfekcyjny. Cena to okazja."
    
    result = nlp_engine.analyze_text_sync(text)

    assert result["battery"] > 0.0
    assert result["screen"] > 0.0
    assert result["camera"] > 0.0
    assert result["price"] > 0.0
