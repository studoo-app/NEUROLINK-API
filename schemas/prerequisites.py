from pydantic import BaseModel, ConfigDict


class Prerequisites(BaseModel):
    reference: str

    model_config = ConfigDict(from_attributes=True)