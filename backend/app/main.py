from fastapi import FastAPI
from pydantic import BaseModel
import os
from .routers import auth, rides
from .routers import ws as ws_routes


class HealthResponse(BaseModel):
    status: str
    service: str
    env: str


def create_app() -> FastAPI:
    app = FastAPI(title=os.getenv("APP_NAME", "Safar Backend"))

    app.include_router(auth.router)
    app.include_router(rides.router)
    app.include_router(ws_routes.router)

    @app.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(
            status="ok",
            service=os.getenv("APP_NAME", "Safar Backend"),
            env=os.getenv("ENV", "dev"),
        )

    return app


app = create_app()
