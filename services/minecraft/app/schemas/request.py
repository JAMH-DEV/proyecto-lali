from typing import Literal

from pydantic import BaseModel, Field, model_validator


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

class SummonRequest(BaseModel):
    mob: str = Field(
        min_length=1,
        pattern=r"^(?:minecraft:)?[a-z0-9_]+$",
    )

    player: str | None = Field(
        default=None,
        min_length=3,
        max_length=16,
        pattern=r"^[A-Za-z0-9_]+$",
    )

    x: float | None = None
    y: float | None = None
    z: float | None = None

    count: int = Field(
        default=1,
        ge=1,
        le=20,
    )

    @model_validator(mode="after")
    def validate_target(self):
        coordinates = (self.x, self.y, self.z)

        has_any_coordinate = any(
            value is not None
            for value in coordinates
        )

        has_all_coordinates = all(
            value is not None
            for value in coordinates
        )

        if has_any_coordinate and not has_all_coordinates:
            raise ValueError(
                "Debes enviar las tres coordenadas: x, y y z."
            )

        if self.player is not None and has_any_coordinate:
            raise ValueError(
                "No puedes indicar jugador y coordenadas al mismo tiempo."
            )

        return self