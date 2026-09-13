from fastapi import APIRouter, Depends

from schemas.enums import Tier
from security.api_key import get_current_api_key

router = APIRouter(
    prefix="/tiers", tags=["Tier"], dependencies=[Depends(get_current_api_key)]
)


@router.get("/", response_model=list[str])
async def list_tiers():
    tiers = [item.value for item in Tier]
    return {"data": tiers}
