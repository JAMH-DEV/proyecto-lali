from typing import Literal

from pydantic import BaseModel, Field


class SayRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=200,
    )


class TimeRequest(BaseModel):
    time: Literal[
        "day",
        "night",
        "noon",
        "midnight",
    ]


class WeatherRequest(BaseModel):
    weather: Literal[
        "clear",
        "rain",
        "thunder",
    ]