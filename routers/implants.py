from fastapi import APIRouter

from schemas.implant import Implant
from schemas.enums import Family, Tier

router = APIRouter(prefix="/implants", tags=["Implants"])


@router.get("/" , response_model=dict[str, list[Implant]])
async def list_implants():

    implants = [
        Implant(reference="REF001", name="Component 1", family=Family.NEURAL, tier=Tier.STANDARD),
        Implant(reference="REF002", name="Component 2", family=Family.SENSORY, tier=Tier.CLINICAL),
        Implant(reference="REF003", name="Component 3", family=Family.MOTOR, tier=Tier.PRIME)
    ]

    return {"data": implants}