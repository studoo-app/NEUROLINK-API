from fastapi import FastAPI

from database import Base, engine
from models import ImplantModel, SideEffectModel, implant_incompatibilities
from routers import implants, hello, tiers, category

app = FastAPI()

api_route_prefix = "/api/v1"

Base.metadata.create_all(bind=engine)

app.include_router(hello.router,prefix=api_route_prefix)
app.include_router(implants.router, prefix=api_route_prefix)
app.include_router(tiers.router, prefix=api_route_prefix)
app.include_router(category.router, prefix=api_route_prefix)
