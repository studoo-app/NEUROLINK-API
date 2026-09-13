from pydantic import BaseModel, ConfigDict, Field

from schemas.prerequisites import Prerequisites
from schemas.SideEffect import SideEffect
from schemas.enums import Tier, Category


class Implant(BaseModel):
    reference: str
    name: str
    category: Category
    tier: Tier
    prerequisites: Prerequisites | None = None
    sideseffects: list[SideEffect] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

