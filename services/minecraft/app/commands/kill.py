import re


PLAYER_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,16}$")
ENTITY_PATTERN = re.compile(
    r"^(?:minecraft:)?[a-z0-9_]+$"
)

VALID_KILL_ACTIONS = {
    "player",
    "mob_type",
    "near_player",
    "near_coordinates",
    "all_players",
    "all_entities",
}


def normalize_player(player: str) -> str:
    normalized_player = player.strip()

    if not PLAYER_PATTERN.fullmatch(normalized_player):
        raise ValueError(
            f"El nombre de jugador '{player}' no es válido."
        )

    return normalized_player


def normalize_entity(entity: str) -> str:
    normalized_entity = entity.strip().lower()

    if not ENTITY_PATTERN.fullmatch(normalized_entity):
        raise ValueError(
            f"El identificador de entidad '{entity}' no es válido."
        )

    if not normalized_entity.startswith("minecraft:"):
        normalized_entity = f"minecraft:{normalized_entity}"

    return normalized_entity


def validate_radius(radius: float) -> float:
    if radius <= 0 or radius > 200:
        raise ValueError(
            "El radio debe ser mayor que 0 y menor o igual a 200."
        )

    return radius


def build_kill_player_command(player: str) -> str:
    normalized_player = normalize_player(player)

    return f"kill {normalized_player}"


def build_kill_mob_type_command(
    mob: str,
) -> str:
    normalized_mob = normalize_entity(mob)

    return f"kill @e[type={normalized_mob}]"


def build_kill_near_player_command(
    player: str,
    radius: float,
    include_players: bool = False,
) -> str:
    normalized_player = normalize_player(player)
    normalized_radius = validate_radius(radius)

    selector_filters = [
        f"distance=..{normalized_radius}",
    ]

    if not include_players:
        selector_filters.append(
            "type=!minecraft:player"
        )

    selector = ",".join(selector_filters)

    return (
        f"execute at {normalized_player} "
        f"run kill @e[{selector}]"
    )


def build_kill_near_coordinates_command(
    x: float,
    y: float,
    z: float,
    radius: float,
    include_players: bool = False,
) -> str:
    normalized_radius = validate_radius(radius)

    selector_filters = [
        f"x={x}",
        f"y={y}",
        f"z={z}",
        f"distance=..{normalized_radius}",
    ]

    if not include_players:
        selector_filters.append(
            "type=!minecraft:player"
        )

    selector = ",".join(selector_filters)

    return f"kill @e[{selector}]"


def build_kill_all_players_command(
    confirm: bool,
) -> str:
    if not confirm:
        raise ValueError(
            "La acción 'all_players' requiere confirm=true."
        )

    return "kill @a"


def build_kill_all_entities_command(
    confirm: bool,
) -> str:
    if not confirm:
        raise ValueError(
            "La acción 'all_entities' requiere confirm=true."
        )

    return "kill @e"


def build_kill_command(
    action: str,
    player: str | None = None,
    mob: str | None = None,
    radius: float | None = None,
    x: float | None = None,
    y: float | None = None,
    z: float | None = None,
    include_players: bool = False,
    confirm: bool = False,
) -> str:
    normalized_action = action.strip().lower()

    if normalized_action not in VALID_KILL_ACTIONS:
        raise ValueError(
            f"La acción '{action}' no está permitida."
        )

    if normalized_action == "player":
        if player is None:
            raise ValueError(
                "La acción 'player' requiere player."
            )

        return build_kill_player_command(player)

    if normalized_action == "mob_type":
        if mob is None:
            raise ValueError(
                "La acción 'mob_type' requiere mob."
            )

        return build_kill_mob_type_command(mob)

    if normalized_action == "near_player":
        if player is None:
            raise ValueError(
                "La acción 'near_player' requiere player."
            )

        if radius is None:
            raise ValueError(
                "La acción 'near_player' requiere radius."
            )

        return build_kill_near_player_command(
            player=player,
            radius=radius,
            include_players=include_players,
        )

    if normalized_action == "near_coordinates":
        if radius is None:
            raise ValueError(
                "La acción 'near_coordinates' requiere radius."
            )

        if x is None or y is None or z is None:
            raise ValueError(
                "Debes proporcionar x, y y z."
            )

        return build_kill_near_coordinates_command(
            x=x,
            y=y,
            z=z,
            radius=radius,
            include_players=include_players,
        )

    if normalized_action == "all_players":
        return build_kill_all_players_command(
            confirm=confirm,
        )

    if normalized_action == "all_entities":
        return build_kill_all_entities_command(
            confirm=confirm,
        )

    raise ValueError(
        f"No se pudo construir la acción '{action}'."
    )