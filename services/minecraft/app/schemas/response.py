from pydantic import BaseModel


class PlayersResponse(BaseModel):
    success: bool
    online: int
    max_players: int
    players: list[str]