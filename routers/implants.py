from fastapi import APIRouter

from schemas.Implant import Implant
from schemas.enums import Tier, Category

router = APIRouter(prefix="/implants", tags=["Implants"])


@router.get("/" , response_model=dict[str, list[Implant]])
async def list_implants():

    implants = [
        Implant(reference="REF001", name="Component 1", category=Category.NEURAL, tier=Tier.STANDARD),
        Implant(reference="REF002", name="Component 2", category=Category.SENSORY, tier=Tier.CLINICAL),
        Implant(reference="REF003", name="Component 3", category=Category.MOTOR, tier=Tier.PRIME)
    ]

    return {"data": implants}