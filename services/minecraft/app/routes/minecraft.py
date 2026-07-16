from fastapi import APIRouter, HTTPException

from app.schemas.request import (
    SayRequest,
    TimeRequest,
    WeatherRequest,
    GiveRequest,
    ClearRequest,
    SummonRequest,
    PlayerActionRequest,
    KillRequest,
    ServerActionRequest,
)
from app.schemas.response import (
    BannedIpsResponse,
    BannedPlayersResponse,
    CommandResponse,
    PlayersResponse,
    ServerStatusResponse,
    SummonResponse,
    WhitelistResponse,
)
from app.services.minecraft_service import MinecraftService

router = APIRouter()

minecraft_service = MinecraftService()

#GETS
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

@router.get(
    "/server/whitelist",
    response_model=WhitelistResponse,
)
def list_whitelist() -> WhitelistResponse:
    try:
        whitelist = minecraft_service.list_whitelist()

        return WhitelistResponse(
            success=True,
            count=whitelist["count"],
            players=whitelist["players"],
        )

    except ConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

@router.get(
    "/server/bans/players",
    response_model=BannedPlayersResponse,
)
def list_banned_players() -> BannedPlayersResponse:
    try:
        bans = minecraft_service.list_banned_players()

        return BannedPlayersResponse(
            success=True,
            count=bans["count"],
            players=bans["players"],
        )

    except ConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

@router.get(
    "/server/bans/ips",
    response_model=BannedIpsResponse,
)
def list_banned_ips() -> BannedIpsResponse:
    try:
        bans = minecraft_service.list_banned_ips()

        return BannedIpsResponse(
            success=True,
            count=bans["count"],
            ips=bans["ips"],
        )

    except ConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error

@router.get(
    "/server/status",
    response_model=ServerStatusResponse,
)
def get_server_status() -> ServerStatusResponse:
    try:
        status = minecraft_service.get_server_status()

        return ServerStatusResponse(
            success=True,
            reachable=status["reachable"],
            online=status["online"],
            max_players=status["max_players"],
            players=status["players"],
        )

    except ConnectionError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        ) from error

#POST
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

@router.post("/summon", response_model=SummonResponse)
def summon(payload: SummonRequest) -> SummonResponse:
    try:
        commands, responses = minecraft_service.summon(
            mob=payload.mob,
            player=payload.player,
            x=payload.x,
            y=payload.y,
            z=payload.z,
            count=payload.count,
        )

        return SummonResponse(
            success=True,
            mob=payload.mob,
            count=payload.count,
            commands=commands,
            responses=responses,
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

@router.post(
    "/player",
    response_model=CommandResponse,
)
def modify_player(
    payload: PlayerActionRequest,
) -> CommandResponse:
    try:
        command, response = minecraft_service.modify_player(
            player=payload.player,
            action=payload.action,
            value=payload.value,
            target_player=payload.target_player,
            x=payload.x,
            y=payload.y,
            z=payload.z,
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

@router.post(
    "/kill",
    response_model=CommandResponse,
)
def kill(
    payload: KillRequest,
) -> CommandResponse:
    try:
        command, response = minecraft_service.kill(
            action=payload.action,
            player=payload.player,
            mob=payload.mob,
            radius=payload.radius,
            x=payload.x,
            y=payload.y,
            z=payload.z,
            include_players=payload.include_players,
            confirm=payload.confirm,
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

@router.post(
    "/server",
    response_model=CommandResponse,
)
def manage_server(
    payload: ServerActionRequest,
) -> CommandResponse:
    try:
        command, response = minecraft_service.manage_server(
            action=payload.action,
            player=payload.player,
            reason=payload.reason,
            confirm=payload.confirm,
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