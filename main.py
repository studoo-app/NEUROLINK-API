from fastapi import FastAPI

from database import Base, engine
from models import ImplantModel, SideEffectModel, implant_incompatibilities
from routers import implants, hello, tiers, category, api_keys
from seed import seed_database

app = FastAPI(title="NeuroLink API", description="API for managing implants and related data", version="1.0.0")

api_route_prefix = "/api/v1"

Base.metadata.create_all(bind=engine)
#seed_database()

app.include_router(hello.router,prefix=api_route_prefix)
app.include_router(api_keys.router,prefix=api_route_prefix)
app.include_router(implants.router, prefix=api_route_prefix)
#app.include_router(tiers.router, prefix=api_route_prefix)
#app.include_router(category.router, prefix=api_route_prefix)
