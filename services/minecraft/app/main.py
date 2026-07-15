from fastapi import FastAPI

from app.core.config import settings
from app.routes.health import router as health_router

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Microservicio encargado de ejecutar acciones "
        "en servidores de Minecraft mediante RCON."
    ),
    version=settings.APP_VERSION,
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    minecraft_router,
    prefix="/api/v1/minecraft",
    tags=["Minecraft"],
)