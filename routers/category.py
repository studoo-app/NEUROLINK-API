from fastapi import APIRouter, Depends

from schemas.enums import Category
from security.api_key import get_current_api_key

router = APIRouter(prefix="/categories", tags=["Category"])

@router.get("/", response_model=list[str],dependencies=[Depends(get_current_api_key)])
async def list_families():
    categories = [item.value for item in Category]
    return {"data": categories}