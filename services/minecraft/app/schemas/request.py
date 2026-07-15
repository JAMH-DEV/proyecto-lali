from pydantic import BaseModel, Field


class SayRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=200,
    )