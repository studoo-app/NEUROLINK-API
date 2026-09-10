from fastapi import FastAPI

from routers import implants, hello

app = FastAPI()

api_route_prefix = "/api/v1"

app.include_router(hello.router,prefix=api_route_prefix)
app.include_router(implants.router, prefix=api_route_prefix)
