from fastapi import APIRouter

from schemas.enums import Tier

router = APIRouter(prefix="/tiers", tags=["Tier"])

@router.get("/", response_model=dict[str, list[str]])
async def list_tiers():
    tiers = [item.value for item in Tier]
    return {"data": tiers}