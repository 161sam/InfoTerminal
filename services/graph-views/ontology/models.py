from typing import List

from pydantic import BaseModel, Field


class PropertySpec(BaseModel):
    name: str
    type: str
    required: bool = False

class EntityType(BaseModel):
    name: str
    label: str
    properties: List[PropertySpec] = Field(default_factory=list)

class RelationType(BaseModel):
    name: str
    type: str
    from_: str = Field(alias="from")
    to: str
    properties: List[PropertySpec] = Field(default_factory=list)

class EntityInstance(BaseModel):
    type: str
    data: dict
