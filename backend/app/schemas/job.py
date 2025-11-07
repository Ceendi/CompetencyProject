from pydantic import BaseModel, AnyUrl, ConfigDict


class JobStatusResponse(BaseModel):
    id: int
    url: AnyUrl
    status: str

    error_message: str | None = None

    film_id: int | None = None

    model_config = ConfigDict(from_attributes=True)