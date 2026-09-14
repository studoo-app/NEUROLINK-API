"""Authentication feature package."""

from .dependencies import get_current_api_key, require_admin
from .models import ApiKeyModel
from .schemas import ApiKeyCreate, ApiKeyCreatedResponse, ApiKeyResponse
from .service import create_api_key

__all__ = [
    "ApiKeyModel",
    "ApiKeyCreate",
    "ApiKeyResponse",
    "ApiKeyCreatedResponse",
    "create_api_key",
    "get_current_api_key",
    "require_admin",
]
