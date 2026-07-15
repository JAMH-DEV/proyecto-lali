VALID_TIMES = {
    "day",
    "night",
    "noon",
    "midnight",
}


def build_time_command(value: str | int) -> str:

    if isinstance(value, int):

        if value < 0 or value > 24000:
            raise ValueError(
                "El valor debe estar entre 0 y 24000."
            )

        return f"time set {value}"

    normalized = value.strip().lower()

    if normalized not in VALID_TIMES:
        raise ValueError(
            "Tiempo inválido."
        )

    return f"time set {normalized}"