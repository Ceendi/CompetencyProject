from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_FILE_PATH = Path(__file__).parent.parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding="utf-8", extra='ignore')

    DATABASE_URL: str

    OPENAI_API_KEY: str | None = None

    # NLP_SPACY_MODEL: str = "en_core_news_sm"
    NLP_SPACY_MODEL: str = "pl_core_news_sm"

    NLP_TRANSFORMER_MODEL: str = "nlptown/bert-base-multilingual-uncased-sentiment"


settings = Settings()
