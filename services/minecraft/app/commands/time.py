VALID_TIMES = {
    "day",
    "night",
    "noon",
    "midnight",
}


def build_time_command(time_value: str) -> str:
    normalized_time = time_value.strip().lower()

    if normalized_time not in VALID_TIMES:
        allowed = ", ".join(sorted(VALID_TIMES))
        raise ValueError(
            f"Tiempo inválido. Valores permitidos: {allowed}"
        )

    return f"time set {normalized_time}"