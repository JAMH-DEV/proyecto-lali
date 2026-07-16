import re


MOB_PATTERN = re.compile(r"^(?:minecraft:)?[a-z0-9_]+$")


def build_summon_command(
    mob: str,
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

    if all(value is None for value in coordinates):
        return f"summon {normalized_mob}"

    if any(value is None for value in coordinates):
        raise ValueError(
            "Debes enviar las tres coordenadas: x, y y z."
        )

    return f"summon {normalized_mob} {x} {y} {z}"