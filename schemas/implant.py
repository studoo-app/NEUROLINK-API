from pydantic import BaseModel, ConfigDict

from schemas.enums import Family, Tier


class Implant(BaseModel):
    reference: str
    name: str
    family: Family
    tier: Tier

    model_config = ConfigDict(from_attributes=True)