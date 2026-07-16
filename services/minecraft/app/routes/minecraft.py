from fastapi import APIRouter, HTTPException

from app.schemas.request import (
    SayRequest,
    TimeRequest,
    WeatherRequest,
    GiveRequest,
    ClearRequest,
)
from app.schemas.response import (
    CommandResponse,
    PlayersResponse,
)
from app.services.minecraft_service import MinecraftService

router = APIRouter()

minecraft_service = MinecraftService()


@router.get("/players", response_model=PlayersResponse)
def list_players() -> PlayersResponse:
    try:
        players = minecraft_service.list_players()

        return PlayersResponse(
            success=True,
            online=players["online"],
            max_players=players["max_players"],
            players=players["players"],
        )

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error


@router.post("/say", response_model=CommandResponse)
def say(payload: SayRequest) -> CommandResponse:
    try:
        command, response = minecraft_service.say(
            payload.message
        )

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

@router.post("/weather", response_model=CommandResponse)
def set_weather(payload: WeatherRequest) -> CommandResponse:
    try:
        command, response = minecraft_service.set_weather(
            payload.weather
        )

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

@router.post("/time", response_model=CommandResponse)
def set_time(payload: TimeRequest) -> CommandResponse:
    try:
        command, response = minecraft_service.set_time(
            payload.value
        )

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

@router.post("/give", response_model=CommandResponse)
def give_item(payload: GiveRequest) -> CommandResponse:
    try:
        command, response = minecraft_service.give_item(
            payload.player,
            payload.item,
            payload.quantity,
        )

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

@router.post("/clear", response_model=CommandResponse)
def clear_inventory(
    payload: ClearRequest,
) -> CommandResponse:
    try:
        command, response = minecraft_service.clear_inventory(
            payload.player,
            payload.item,
            payload.quantity,
        )

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