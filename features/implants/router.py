from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from features.auth.dependencies import get_current_api_key
from features.implants.models import ImplantModel
from features.implants.schemas import Implant
from features.implants.service import serialize_implant

router = APIRouter(
    prefix="/implants",
    tags=["Implant"],
    dependencies=[Depends(get_current_api_key)],
)


@router.get("/", response_model=list[Implant])
async def list_implants(db: Annotated[Session, Depends(get_db)]):
    implants = db.scalars(select(ImplantModel).order_by(ImplantModel.reference)).all()
    return [serialize_implant(implant) for implant in implants]


@router.get("/{reference}", response_model=Implant)
async def get_implant(
    reference: str,
    db: Annotated[Session, Depends(get_db)],
):
    implant = db.scalar(
        select(ImplantModel).where(ImplantModel.reference == reference)
    )
    if implant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Implant '{reference}' not found",
        )
    return serialize_implant(implant)