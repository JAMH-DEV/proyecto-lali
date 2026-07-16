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