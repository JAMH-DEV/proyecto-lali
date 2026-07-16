import re


PLAYER_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,16}$")
ITEM_PATTERN = re.compile(r"^(?:minecraft:)?[a-z0-9_]+$")


def build_clear_command(
    player: str,
    item: str | None = None,
    quantity: int | None = None,
) -> str:
    normalized_player = player.strip()

    if not PLAYER_PATTERN.fullmatch(normalized_player):
        raise ValueError(
            "El nombre del jugador no es válido."
        )

    if item is None:
        if quantity is not None:
            raise ValueError(
                "No puedes indicar una cantidad sin especificar un objeto."
            )

        return f"clear {normalized_player}"

    normalized_item = item.strip().lower()

    if not ITEM_PATTERN.fullmatch(normalized_item):
        raise ValueError(
            "El identificador del objeto no es válido."
        )

    if not normalized_item.startswith("minecraft:"):
        normalized_item = f"minecraft:{normalized_item}"

    if quantity is None:
        return (
            f"clear {normalized_player} "
            f"{normalized_item}"
        )

    if quantity < 1 or quantity > 640:
        raise ValueError(
            "La cantidad debe estar entre 1 y 640."
        )

    return (
        f"clear {normalized_player} "
        f"{normalized_item} {quantity}"
    )