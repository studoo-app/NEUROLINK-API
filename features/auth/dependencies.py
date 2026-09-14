import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from core.enums import ApiKeyRole
from core.security import extract_key_id, hash_api_key
from features.auth.models import ApiKeyModel

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_api_key(
    api_key: Annotated[str | None, Depends(api_key_header)],
    db: Annotated[Session, Depends(get_db)],
) -> ApiKeyModel:
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    key_id = extract_key_id(api_key)
    if key_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    statement = select(ApiKeyModel).where(ApiKeyModel.key_id == key_id)
    db_api_key = db.scalar(statement)

    if db_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    if not db_api_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key disabled",
        )

    if not secrets.compare_digest(hash_api_key(api_key), db_api_key.key_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return db_api_key


def require_admin(
    api_key: Annotated[ApiKeyModel, Depends(get_current_api_key)],
) -> ApiKeyModel:
    if api_key.role != ApiKeyRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin API key required",
        )

    return api_key