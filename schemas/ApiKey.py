from pydantic import BaseModel, ConfigDict

from schemas.enums import ApiKeyRole


class ApiKeyCreate(BaseModel):
    name: str
    role: ApiKeyRole


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    key_id: str
    role: ApiKeyRole
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class ApiKeyCreatedResponse(ApiKeyResponse):
    api_key: str