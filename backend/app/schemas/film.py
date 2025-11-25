from pydantic import BaseModel, AnyUrl, Field, ConfigDict

from .analysis import Analysis


class FilmBase(BaseModel):
    url: AnyUrl = Field(..., max_length=200, description="Full URL to (YouTube, TikTok, Instagram)")


class FilmCreate(FilmBase):
    pass


class Film(FilmBase):
    id: int
    title: str | None = None
    platform: str | None = None
    transcribed_text: str | None = None

    analysis: Analysis | None = None

    model_config = ConfigDict(from_attributes=True)
