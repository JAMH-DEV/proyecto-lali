from pydantic import BaseModel, Field
from typing import Literal


class SayRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=200,
    )

class WeatherRequest(BaseModel):
    weather: Literal[
        "clear",
        "rain",
        "thunder",
    ]