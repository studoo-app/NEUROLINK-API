from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import ApiKeyModel
from schemas.ApiKey import ApiKeyCreate, ApiKeyCreatedResponse, ApiKeyResponse
from security.api_key import require_admin
from services.api_key import create_api_key

router = APIRouter(
    prefix="/authentification",
    tags=["Authentification"],
    dependencies=[Depends(require_admin)],
)


@router.post(
    "/generate-key",
    response_model=ApiKeyCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_key(
    payload: ApiKeyCreate,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    db_key, api_key = create_api_key(
        db=db,
        name=payload.name,
        role=payload.role,
    )

    return ApiKeyCreatedResponse(
        id=db_key.id,
        name=db_key.name,
        key_id=db_key.key_id,
        role=db_key.role,
        is_active=db_key.is_active,
        api_key=api_key,
    )


@router.get("/list-keys", response_model=list[ApiKeyResponse])
def list_api_keys(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    statement = select(ApiKeyModel)

    return db.scalars(statement).all()


@router.delete(
    "/revoke/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def revoke_api_key(
    key_id: str,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    statement = select(ApiKeyModel).where(ApiKeyModel.key_id == key_id)

    api_key = db.scalar(statement)

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )

    api_key.is_active = False

    db.commit()
