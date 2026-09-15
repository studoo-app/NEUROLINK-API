from fastapi import APIRouter, Depends

from core import Category
from features.auth.dependencies import get_current_api_key

router = APIRouter(
    prefix="/categories",
    tags=["Category"],
    dependencies=[Depends(get_current_api_key)],
)


@router.get("/")
async def list_categories():
    return [category.value for category in Category]