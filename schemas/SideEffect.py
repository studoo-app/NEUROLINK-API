from pydantic import BaseModel, ConfigDict


class SideEffect(BaseModel):
    reference: str
    name: str
    severity: str
    description: str

    model_config = ConfigDict(from_attributes=True)
