from fastapi import FastAPI

from app.startup import run_startup
from core.database import Base, engine
from features.auth.router import router as auth_router
from features.health_check.router import router as health_router
from features.implants.router import router as implants_router
from features.category.router import router as category_router

app = FastAPI(
    title="NeuroLink API",
    description="API for managing implants and related data",
    version="1.0.0",
)

api_route_prefix = "/api/v1"

Base.metadata.create_all(bind=engine)
run_startup()

app.include_router(health_router, prefix=api_route_prefix)
app.include_router(auth_router, prefix=api_route_prefix)
app.include_router(implants_router, prefix=api_route_prefix)
app.include_router(category_router, prefix=api_route_prefix)