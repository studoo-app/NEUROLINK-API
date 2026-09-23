from fastapi import APIRouter, Depends

from features.auth import require_admin
from features.tools.service import generate_additionnal_implants

router = APIRouter(
    prefix="/tools",
    tags=["Tools"]
)


@router.get("/health-check")
async def health_check():
    return {"message": "Welcome to NeuroLink Corp Components API. Service is running smoothly!"}


@router.get("/generate-implants",dependencies=[Depends(require_admin)])
async def generate_implants():
    generate_additionnal_implants()
    return {"message": "Mise à jour du catalogue d'implants. "}