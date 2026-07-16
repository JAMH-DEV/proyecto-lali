import re


PLAYER_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,16}$")

VALID_SERVER_ACTIONS = {
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
}


def normalize_player(player: str) -> str:
    normalized_player = player.strip()

    if not PLAYER_PATTERN.fullmatch(normalized_player):
        raise ValueError(
            f"El nombre de jugador '{player}' no es válido."
        )

    return normalized_player


def normalize_reason(reason: str | None) -> str | None:
    if reason is None:
        return None

    normalized_reason = (
        reason
        .replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )

    if not normalized_reason:
        return None

    return normalized_reason[:150]


def build_server_command(
    action: str,
    player: str | None = None,
    reason: str | None = None,
    confirm: bool = False,
) -> str:
    normalized_action = action.strip().lower()

    if normalized_action not in VALID_SERVER_ACTIONS:
        raise ValueError(
            f"La acción '{action}' no está permitida."
        )

    if normalized_action == "whitelist_on":
        return "whitelist on"

    if normalized_action == "whitelist_off":
        if not confirm:
            raise ValueError(
                "La acción 'whitelist_off' requiere confirm=true."
            )

        return "whitelist off"

    if normalized_action == "whitelist_reload":
        return "whitelist reload"

    if normalized_action in {
        "whitelist_add",
        "whitelist_remove",
        "op",
        "deop",
        "kick",
        "ban",
        "pardon",
    }:
        if player is None:
            raise ValueError(
                f"La acción '{normalized_action}' requiere player."
            )

        normalized_player = normalize_player(player)

        if normalized_action == "whitelist_add":
            return f"whitelist add {normalized_player}"

        if normalized_action == "whitelist_remove":
            return f"whitelist remove {normalized_player}"

        if normalized_action == "op":
            if not confirm:
                raise ValueError(
                    "La acción 'op' requiere confirm=true."
                )

            return f"op {normalized_player}"

        if normalized_action == "deop":
            return f"deop {normalized_player}"

        if normalized_action == "kick":
            normalized_reason = normalize_reason(reason)

            if normalized_reason:
                return (
                    f"kick {normalized_player} "
                    f"{normalized_reason}"
                )

            return f"kick {normalized_player}"

        if normalized_action == "ban":
            if not confirm:
                raise ValueError(
                    "La acción 'ban' requiere confirm=true."
                )

            normalized_reason = normalize_reason(reason)

            if normalized_reason:
                return (
                    f"ban {normalized_player} "
                    f"{normalized_reason}"
                )

            return f"ban {normalized_player}"

        if normalized_action == "pardon":
            return f"pardon {normalized_player}"

    if normalized_action == "save":
        return "save-all flush"

    if normalized_action == "stop":
        if not confirm:
            raise ValueError(
                "La acción 'stop' requiere confirm=true."
            )

        return "stop"

    raise ValueError(
        f"No se pudo construir la acción '{action}'."
    )