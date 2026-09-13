from pydantic import BaseModel, ConfigDict, Field

from schemas.enums import Category, Tier
from schemas.Prerequisites import Prerequisites
from schemas.SideEffect import SideEffect


class Implant(BaseModel):
    reference: str
    name: str
    description: str
    category: Category
    tier: Tier
    prerequisites: Prerequisites | None = Prerequisites()
    sideseffects: list[SideEffect] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
