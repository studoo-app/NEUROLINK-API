from fastapi import APIRouter

router = APIRouter(prefix="/hello")

@router.get("/")
async def root():
    return {"message": "Welcome to NeuroLink Corp Components API!"}

@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}