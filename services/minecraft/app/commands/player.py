import math
import re


PLAYER_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,16}$")

VALID_PLAYER_ACTIONS = {
    "heal",
    "damage",
    "set_max_health",
    "add_absorption",
    "clear_absorption",
    "fill_food",
    "apply_hunger",
    "teleport_coordinates",
    "teleport_player",
}


def normalize_player(player: str) -> str:
    normalized_player = player.strip()

    if not PLAYER_PATTERN.fullmatch(normalized_player):
        raise ValueError(
            f"El nombre de jugador '{player}' no es válido."
        )

    return normalized_player


def build_heal_command(player: str) -> str:
    normalized_player = normalize_player(player)

    return (
        f"effect give {normalized_player} "
        "minecraft:instant_health 1 4 true"
    )


def build_damage_command(
    player: str,
    amount: int,
) -> str:
    normalized_player = normalize_player(player)

    if amount < 1 or amount > 100:
        raise ValueError(
            "El daño debe estar entre 1 y 100 puntos."
        )

    return (
        f"damage {normalized_player} "
        f"{amount} minecraft:generic"
    )


def build_set_max_health_command(
    player: str,
    amount: int,
) -> str:
    normalized_player = normalize_player(player)

    if amount < 1 or amount > 2048:
        raise ValueError(
            "La vida máxima debe estar entre 1 y 2048 puntos."
        )

    return (
        f"attribute {normalized_player} "
        "minecraft:generic.max_health "
        f"base set {amount}"
    )


def build_add_absorption_command(
    player: str,
    golden_hearts: int,
) -> str:
    normalized_player = normalize_player(player)

    if golden_hearts < 2 or golden_hearts > 40:
        raise ValueError(
            "Los corazones dorados deben estar entre 2 y 40."
        )

    if golden_hearts % 2 != 0:
        raise ValueError(
            "Los corazones dorados deben indicarse de 2 en 2."
        )

    amplifier = math.ceil(golden_hearts / 2) - 1

    return (
        f"effect give {normalized_player} "
        f"minecraft:absorption 600 {amplifier} true"
    )


def build_clear_absorption_command(player: str) -> str:
    normalized_player = normalize_player(player)

    return (
        f"effect clear {normalized_player} "
        "minecraft:absorption"
    )


def build_fill_food_command(player: str) -> str:
    normalized_player = normalize_player(player)

    return (
        f"effect give {normalized_player} "
        "minecraft:saturation 1 20 true"
    )


def build_hunger_command(
    player: str,
    duration: int,
) -> str:
    normalized_player = normalize_player(player)

    if duration < 1 or duration > 300:
        raise ValueError(
            "La duración del hambre debe estar entre 1 y 300 segundos."
        )

    return (
        f"effect give {normalized_player} "
        f"minecraft:hunger {duration} 9 true"
    )


def build_teleport_coordinates_command(
    player: str,
    x: float,
    y: float,
    z: float,
) -> str:
    normalized_player = normalize_player(player)

    return (
        f"tp {normalized_player} "
        f"{x} {y} {z}"
    )


def build_teleport_player_command(
    player: str,
    target_player: str,
) -> str:
    normalized_player = normalize_player(player)
    normalized_target = normalize_player(target_player)

    if normalized_player == normalized_target:
        raise ValueError(
            "El jugador de origen y el destino no pueden ser el mismo."
        )

    return (
        f"tp {normalized_player} "
        f"{normalized_target}"
    )


def build_player_action_command(
    player: str,
    action: str,
    value: int | None = None,
    target_player: str | None = None,
    x: float | None = None,
    y: float | None = None,
    z: float | None = None,
) -> str:
    normalized_action = action.strip().lower()

    if normalized_action not in VALID_PLAYER_ACTIONS:
        raise ValueError(
            f"La acción '{action}' no está permitida."
        )

    if normalized_action == "heal":
        return build_heal_command(player)

    if normalized_action == "damage":
        if value is None:
            raise ValueError(
                "La acción 'damage' requiere un valor."
            )

        return build_damage_command(player, value)

    if normalized_action == "set_max_health":
        if value is None:
            raise ValueError(
                "La acción 'set_max_health' requiere un valor."
            )

        return build_set_max_health_command(
            player,
            value,
        )

    if normalized_action == "add_absorption":
        if value is None:
            raise ValueError(
                "La acción 'add_absorption' requiere un valor."
            )

        return build_add_absorption_command(
            player,
            value,
        )

    if normalized_action == "clear_absorption":
        return build_clear_absorption_command(player)

    if normalized_action == "fill_food":
        return build_fill_food_command(player)

    if normalized_action == "apply_hunger":
        if value is None:
            raise ValueError(
                "La acción 'apply_hunger' requiere una duración."
            )

        return build_hunger_command(
            player,
            value,
        )

    if normalized_action == "teleport_coordinates":
        if x is None or y is None or z is None:
            raise ValueError(
                "Debes proporcionar las coordenadas x, y y z."
            )

        return build_teleport_coordinates_command(
            player,
            x,
            y,
            z,
        )

    if normalized_action == "teleport_player":
        if target_player is None:
            raise ValueError(
                "La acción 'teleport_player' requiere target_player."
            )

        return build_teleport_player_command(
            player,
            target_player,
        )

    raise ValueError(
        f"No se pudo construir la acción '{action}'."
    )