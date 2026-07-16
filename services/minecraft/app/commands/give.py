import re


PLAYER_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,16}$")
ITEM_PATTERN = re.compile(
    r"^(?:minecraft:)?[a-z0-9_]+$"
)


def build_give_command(
    player: str,
    item: str,
    quantity: int,
) -> str:
    normalized_player = player.strip()
    normalized_item = item.strip().lower()

    if not PLAYER_PATTERN.fullmatch(normalized_player):
        raise ValueError(
            "El nombre del jugador no es válido."
        )

    if not ITEM_PATTERN.fullmatch(normalized_item):
        raise ValueError(
            "El identificador del objeto no es válido."
        )

    if quantity < 1 or quantity > 640:
        raise ValueError(
            "La cantidad debe estar entre 1 y 640."
        )

    if not normalized_item.startswith("minecraft:"):
        normalized_item = f"minecraft:{normalized_item}"

    return (
        f"give {normalized_player} "
        f"{normalized_item} {quantity}"
    )