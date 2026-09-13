from pydantic import BaseModel, ConfigDict

class SideEffect(BaseModel):
    reference: str

    model_config = ConfigDict(from_attributes=True)