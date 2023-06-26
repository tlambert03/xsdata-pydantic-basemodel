from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TypeA(BaseModel):
    one: str
    two: float


class TypeB(TypeA):
    one: str
    three: bool = Field(default=True)


class TypeC(TypeB):
    four: List[datetime] = Field(
        default_factory=list, metadata={"format": "%d %B %Y %H:%M"}
    )
    any: Optional[object] = Field(default=None, metadata={"type": "Wildcard"})
