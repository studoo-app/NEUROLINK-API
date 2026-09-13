from fastapi import APIRouter, Depends

from database import get_db
from models import ImplantModel
from schemas.Implant import Implant
from schemas.Prerequisites import Prerequisites
from security.api_key import get_current_api_key

router = APIRouter(
    prefix="/implants", tags=["Implant"], dependencies=[Depends(get_current_api_key)]
)


@router.get("/", response_model=list[Implant])
async def list_implants():

    db = next(get_db())

    implants = db.query(ImplantModel).all()

    return [
        Implant(
            reference=implant.reference,
            name=implant.name,
            description=implant.description,
            category=implant.category,
            tier=implant.tier,
            prerequisites=Prerequisites(
                **(implant.prerequisites or {}),
                incompatibleImplants=[
                    incompatible_implant.reference
                    for incompatible_implant in implant.incompatible_implants
                ],
            ),
            sideseffects=implant.side_effects,
        )
        for implant in implants
    ]
