# Disease sc
import datetime

from pydantic import BaseModel, Field


class DiseasesInCreate(BaseModel):
    name: str = Field(...)
    reason: str
    recommendation: str


class DiseasesInResponse(BaseModel):
    diseases_name: str
    time: datetime.datetime
    reason: str
    recommendation: str
    image_url: str


class DiseaseOut(BaseModel):
    name: str
    reason: str
    recommendation: str
