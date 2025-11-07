from pydantic import BaseModel, Field, ConfigDict

class AnalysisBase(BaseModel):
    battery: float | None = Field(default=None, ge=-1.0, le=1.0)
    screen: float | None = Field(default=None, ge=-1.0, le=1.0)
    memory: float | None = Field(default=None, ge=-1.0, le=1.0)
    ram_memory: float | None = Field(default=None, ge=-1.0, le=1.0)
    camera: float | None = Field(default=None, ge=-1.0, le=1.0)
    performance: float | None = Field(default=None, ge=-1.0, le=1.0)
    design: float | None = Field(default=None, ge=-1.0, le=1.0)
    quick_charge: float | None = Field(default=None, ge=-1.0, le=1.0)
    audio: float | None = Field(default=None, ge=-1.0, le=1.0)
    price: float | None = Field(default=None, ge=-1.0, le=1.0)


class AnalysisCreate(AnalysisBase):
    pass


class Analysis(AnalysisBase):
    id: int
    film_id: int

    model_config = ConfigDict(from_attributes=True)
