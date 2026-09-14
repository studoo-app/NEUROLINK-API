from pydantic import BaseModel, ConfigDict, Field

from core.enums import Category, Tier


class Prerequisites(BaseModel):
    minAge: int | None = None
    maxAge: int | None = None
    minSize: int | None = None
    maxSize: int | None = None
    minWeight: int | None = None
    maxWeight: int | None = None
    incompatibleImplants: list[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class SideEffect(BaseModel):
    reference: str
    name: str
    severity: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class Implant(BaseModel):
    reference: str
    name: str
    description: str
    category: Category
    tier: Tier
    prerequisites: Prerequisites | None = Prerequisites()
    sideseffects: list[SideEffect] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)