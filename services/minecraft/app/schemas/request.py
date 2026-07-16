from typing import Literal

from pydantic import BaseModel, Field


class SayRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=200,
    )


class TimeRequest(BaseModel):
    value: Literal[
        "day",
        "night",
        "noon",
        "midnight",
    ] | int = Field(
        description="Puede ser una palabra clave o un valor entre 0 y 24000."
    )


class WeatherRequest(BaseModel):
    weather: Literal[
        "clear",
        "rain",
        "thunder",
    ]


class GiveRequest(BaseModel):
    player: str = Field(
        min_length=3,
        max_length=16,
        pattern=r"^[A-Za-z0-9_]+$",
    )
    item: str = Field(
        min_length=1,
        pattern=r"^(?:minecraft:)?[a-z0-9_]+$",
    )
    quantity: int = Field(
        ge=1,
        le=640,
    )