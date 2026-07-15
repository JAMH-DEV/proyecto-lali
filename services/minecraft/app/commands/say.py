def build_say_command(message: str) -> str:
    clean_message = message.replace("\n", " ").replace("\r", " ").strip()

    if not clean_message:
        raise ValueError("El mensaje no puede estar vacío")

    return f"say {clean_message[:200]}"