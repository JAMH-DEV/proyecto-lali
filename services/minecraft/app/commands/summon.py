import re


MOB_PATTERN = re.compile(r"^(?:minecraft:)?[a-z0-9_]+$")
PLAYER_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,16}$")


def build_summon_command(
    mob: str,
    player: str | None = None,
    x: float | None = None,
    y: float | None = None,
    z: float | None = None,
) -> str:
    normalized_mob = mob.strip().lower()

    if not MOB_PATTERN.fullmatch(normalized_mob):
        raise ValueError("El identificador del mob no es válido.")

    if not normalized_mob.startswith("minecraft:"):
        normalized_mob = f"minecraft:{normalized_mob}"

    coordinates = (x, y, z)
    has_coordinates = any(value is not None for value in coordinates)

    if player is not None and has_coordinates:
        raise ValueError(
            "No puedes indicar jugador y coordenadas al mismo tiempo."
        )

    if player is not None:
        normalized_player = player.strip()

        if not PLAYER_PATTERN.fullmatch(normalized_player):
            raise ValueError("El nombre del jugador no es válido.")

        return (
            f"execute at {normalized_player} "
            f"run summon {normalized_mob} ~ ~ ~"
        )

    if has_coordinates:
        if any(value is None for value in coordinates):
            raise ValueError(
                "Debes enviar las tres coordenadas: x, y y z."
            )

        return f"summon {normalized_mob} {x} {y} {z}"

    return f"summon {normalized_mob}"