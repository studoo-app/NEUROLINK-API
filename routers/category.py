from fastapi import APIRouter

from schemas.enums import Category

router = APIRouter(prefix="/categories", tags=["Category"])

@router.get("/", response_model=list[str])
async def list_families():
    categories = [item.value for item in Category]
    return {"data": categories}