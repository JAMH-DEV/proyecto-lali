from pydantic import BaseModel


class CommandResponse(BaseModel):
    success: bool
    command: str
    response: str