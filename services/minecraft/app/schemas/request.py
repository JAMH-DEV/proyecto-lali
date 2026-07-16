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


class PlayerActionRequest(BaseModel):
    player: str = Field(
        min_length=3,
        max_length=16,
        pattern=r"^[A-Za-z0-9_]+$",
    )

    action: Literal[
        "heal",
        "damage",
        "set_max_health",
        "add_absorption",
        "clear_absorption",
        "fill_food",
        "apply_hunger",
    ]

    value: int | None = Field(
        default=None,
        ge=1,
        le=100,
    )

    @model_validator(mode="after")
    def validate_value(self):
        actions_requiring_value = {
            "damage",
            "set_max_health",
            "add_absorption",
            "apply_hunger",
        }

        if self.action in actions_requiring_value and self.value is None:
            raise ValueError(
                f"La acción '{self.action}' requiere un valor."
            )

        if self.action not in actions_requiring_value and self.value is not None:
            raise ValueError(
                f"La acción '{self.action}' no acepta un valor."
            )

        return self

class PlayerActionRequest(BaseModel):
    player: str = Field(
        min_length=3,
        max_length=16,
        pattern=r"^[A-Za-z0-9_]+$",
    )

    action: Literal[
        "heal",
        "damage",
        "set_max_health",
        "add_absorption",
        "clear_absorption",
        "fill_food",
        "apply_hunger",
        "teleport_coordinates",
        "teleport_player",
    ]

    value: int | None = None

    target_player: str | None = Field(
        default=None,
        min_length=3,
        max_length=16,
        pattern=r"^[A-Za-z0-9_]+$",
    )

    x: float | None = None
    y: float | None = None
    z: float | None = None

    @model_validator(mode="after")
    def validate_action_parameters(self):
        value_actions = {
            "damage",
            "set_max_health",
            "add_absorption",
            "apply_hunger",
        }

        actions_without_parameters = {
            "heal",
            "clear_absorption",
            "fill_food",
        }

        coordinates = (
            self.x,
            self.y,
            self.z,
        )

        has_any_coordinate = any(
            coordinate is not None
            for coordinate in coordinates
        )

        has_all_coordinates = all(
            coordinate is not None
            for coordinate in coordinates
        )

        if self.action in value_actions:
            if self.value is None:
                raise ValueError(
                    f"La acción '{self.action}' requiere value."
                )

            if self.target_player is not None:
                raise ValueError(
                    f"La acción '{self.action}' no acepta target_player."
                )

            if has_any_coordinate:
                raise ValueError(
                    f"La acción '{self.action}' no acepta coordenadas."
                )

        elif self.action in actions_without_parameters:
            if self.value is not None:
                raise ValueError(
                    f"La acción '{self.action}' no acepta value."
                )

            if self.target_player is not None:
                raise ValueError(
                    f"La acción '{self.action}' no acepta target_player."
                )

            if has_any_coordinate:
                raise ValueError(
                    f"La acción '{self.action}' no acepta coordenadas."
                )

        elif self.action == "teleport_coordinates":
            if not has_all_coordinates:
                raise ValueError(
                    "Debes proporcionar las coordenadas x, y y z."
                )

            if self.target_player is not None:
                raise ValueError(
                    "No envíes target_player al usar coordenadas."
                )

            if self.value is not None:
                raise ValueError(
                    "La acción 'teleport_coordinates' no acepta value."
                )

        elif self.action == "teleport_player":
            if self.target_player is None:
                raise ValueError(
                    "La acción 'teleport_player' requiere target_player."
                )

            if has_any_coordinate:
                raise ValueError(
                    "No envíes coordenadas al usar target_player."
                )

            if self.value is not None:
                raise ValueError(
                    "La acción 'teleport_player' no acepta value."
                )

        return self

class KillRequest(BaseModel):
    action: Literal[
        "player",
        "mob_type",
        "near_player",
        "near_coordinates",
        "all_players",
        "all_entities",
    ]

    player: str | None = Field(
        default=None,
        min_length=3,
        max_length=16,
        pattern=r"^[A-Za-z0-9_]+$",
    )

    mob: str | None = Field(
        default=None,
        min_length=1,
        pattern=r"^(?:minecraft:)?[a-z0-9_]+$",
    )

    radius: float | None = Field(
        default=None,
        gt=0,
        le=200,
    )

    x: float | None = None
    y: float | None = None
    z: float | None = None

    include_players: bool = False
    confirm: bool = False

    @model_validator(mode="after")
    def validate_action_parameters(self):
        coordinates = (
            self.x,
            self.y,
            self.z,
        )

        has_any_coordinate = any(
            coordinate is not None
            for coordinate in coordinates
        )

        has_all_coordinates = all(
            coordinate is not None
            for coordinate in coordinates
        )

        if self.action == "player":
            if self.player is None:
                raise ValueError(
                    "La acción 'player' requiere player."
                )

            if self.mob is not None:
                raise ValueError(
                    "La acción 'player' no acepta mob."
                )

            if self.radius is not None or has_any_coordinate:
                raise ValueError(
                    "La acción 'player' no acepta área."
                )

        elif self.action == "mob_type":
            if self.mob is None:
                raise ValueError(
                    "La acción 'mob_type' requiere mob."
                )

            if self.player is not None:
                raise ValueError(
                    "La acción 'mob_type' no acepta player."
                )

            if self.radius is not None or has_any_coordinate:
                raise ValueError(
                    "La acción 'mob_type' no acepta área."
                )

        elif self.action == "near_player":
            if self.player is None:
                raise ValueError(
                    "La acción 'near_player' requiere player."
                )

            if self.radius is None:
                raise ValueError(
                    "La acción 'near_player' requiere radius."
                )

            if has_any_coordinate:
                raise ValueError(
                    "La acción 'near_player' no acepta coordenadas."
                )

        elif self.action == "near_coordinates":
            if self.radius is None:
                raise ValueError(
                    "La acción 'near_coordinates' requiere radius."
                )

            if not has_all_coordinates:
                raise ValueError(
                    "Debes proporcionar x, y y z."
                )

            if self.player is not None:
                raise ValueError(
                    "La acción 'near_coordinates' no acepta player."
                )

        elif self.action in {
            "all_players",
            "all_entities",
        }:
            if not self.confirm:
                raise ValueError(
                    f"La acción '{self.action}' requiere confirm=true."
                )

            if (
                self.player is not None
                or self.mob is not None
                or self.radius is not None
                or has_any_coordinate
            ):
                raise ValueError(
                    f"La acción '{self.action}' no acepta filtros."
                )

        return self

class ServerActionRequest(BaseModel):
        action: Literal[
            "whitelist_on",
            "whitelist_off",
            "whitelist_add",
            "whitelist_remove",
            "whitelist_reload",
            "op",
            "deop",
            "kick",
            "ban",
            "pardon",
            "save",
            "stop",
        ]

        player: str | None = Field(
            default=None,
            min_length=3,
            max_length=16,
            pattern=r"^[A-Za-z0-9_]+$",
        )

        reason: str | None = Field(
            default=None,
            max_length=150,
        )

        confirm: bool = False

        @model_validator(mode="after")
        def validate_action_parameters(self):
            player_actions = {
                "whitelist_add",
                "whitelist_remove",
                "op",
                "deop",
                "kick",
                "ban",
                "pardon",
            }

            dangerous_actions = {
                "whitelist_off",
                "op",
                "ban",
                "stop",
            }

            if self.action in player_actions:
                if self.player is None:
                    raise ValueError(
                        f"La acción '{self.action}' requiere player."
                    )

            elif self.player is not None:
                raise ValueError(
                    f"La acción '{self.action}' no acepta player."
                )

            if self.reason is not None and self.action not in {
                "kick",
                "ban",
            }:
                raise ValueError(
                    "reason solo está permitido para kick y ban."
                )

            if self.action in dangerous_actions and not self.confirm:
                raise ValueError(
                    f"La acción '{self.action}' requiere confirm=true."
                )

            return self