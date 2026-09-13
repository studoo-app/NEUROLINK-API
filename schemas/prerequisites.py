from pydantic import BaseModel, ConfigDict


class Prerequisites(BaseModel):
    minAge: int | None = None
    maxAge: int | None = None
    minSize: int | None = None
    maxSize: int | None = None
    minWeight: int | None = None
    maxWeight: int | None = None
    incompatibleImplants: list[str] = []
    model_config = ConfigDict(from_attributes=True)