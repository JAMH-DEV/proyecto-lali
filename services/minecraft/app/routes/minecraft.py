from fastapi import APIRouter, HTTPException

from app.schemas.response import CommandResponse
from app.services.minecraft_service import MinecraftService

router = APIRouter()

minecraft_service = MinecraftService()


@router.get("/players", response_model=CommandResponse)
def list_players() -> CommandResponse:
    try:
        response = minecraft_service.list_players()

        return CommandResponse(
            success=True,
            command="list",
            response=response,
        )

    except ConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error