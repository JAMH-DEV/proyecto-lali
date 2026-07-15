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