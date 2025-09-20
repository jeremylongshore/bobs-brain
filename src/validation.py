from typing import Optional

from pydantic import BaseModel, Field


class QueryBody(BaseModel):
    query: str = Field(min_length=1)
    context: Optional[str] = None


class LearnBody(BaseModel):
    correction: str = Field(min_length=1)
    context: Optional[str] = None
