from fastapi import APIRouter, HTTPException

from app.schemas.response import CommandResponse
from app.services.minecraft_service import MinecraftService
from app.schemas.request import SayRequest

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


@router.post("/say", response_model=CommandResponse)
def say(payload: SayRequest) -> CommandResponse:
    try:
        command, response = minecraft_service.say(payload.message)

        return CommandResponse(
            success=True,
            command=command,
            response=response,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except ConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error