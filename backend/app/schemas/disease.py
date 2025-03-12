# Disease schema
from pydantic import BaseModel, Field


class DiseasesInCreate(BaseModel):
    name: str = Field(...)
    reason: str
    recommendation: str
