from typing import Literal

from pydantic import BaseModel, Field, model_validator,


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

class ClearRequest(BaseModel):
    player: str = Field(
        min_length=3,
        max_length=16,
        pattern=r"^[A-Za-z0-9_]+$",
    )
    item: str | None = Field(
        default=None,
        pattern=r"^(?:minecraft:)?[a-z0-9_]+$",
    )
    quantity: int | None = Field(
        default=None,
        ge=1,
        le=640,
    )

    @model_validator(mode="after")
    def validate_quantity_requires_item(self):
        if self.quantity is not None and self.item is None:
            raise ValueError(
                "No puedes indicar una cantidad sin especificar un objeto."
            )

        return self