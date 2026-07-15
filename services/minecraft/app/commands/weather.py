VALID_WEATHER = {
    "clear",
    "rain",
    "thunder",
}


def build_weather_command(weather: str) -> str:
    normalized_weather = weather.strip().lower()

    if normalized_weather not in VALID_WEATHER:
        allowed = ", ".join(sorted(VALID_WEATHER))
        raise ValueError(
            f"Clima inválido. Valores permitidos: {allowed}"
        )

    return f"weather {normalized_weather}"