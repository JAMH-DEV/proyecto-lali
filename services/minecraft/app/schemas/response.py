from pydantic import BaseModel


class CommandResponse(BaseModel):
    success: bool
    command: str
    response: str


class PlayersResponse(BaseModel):
    success: bool
    online: int
    max_players: int
    players: list[str]

class SummonResponse(BaseModel):
    success: bool
    mob: str
    count: int
    commands: list[str]
    responses: list[str]

class WhitelistResponse(BaseModel):
    success: bool
    count: int
    players: list[str]


class BannedPlayersResponse(BaseModel):
    success: bool
    count: int
    players: list[str]


class BannedIpsResponse(BaseModel):
    success: bool
    count: int
    ips: list[str]


class ServerStatusResponse(BaseModel):
    success: bool
    reachable: bool
    online: int
    max_players: int
    players: list[str]