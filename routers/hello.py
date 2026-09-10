from fastapi import APIRouter

router = APIRouter(prefix="/hello")

@router.get("/")
async def root():
    return {"message": "Welcome to NeuroLink Corp Components API!"}

@router.get("/health")
async def health():
    return {"message": "API is running smoothly!"}