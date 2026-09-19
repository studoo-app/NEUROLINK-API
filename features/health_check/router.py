from fastapi import APIRouter

router = APIRouter()


@router.get("/health-check")
async def health_check():
    return {"message": "Welcome to NeuroLink Corp Components API. Service is running smoothly!"}
