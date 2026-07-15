from mctools import RCONClient

from app.core.config import settings


class MinecraftRconClient:
    def __init__(self) -> None:
        self.host = settings.MINECRAFT_RCON_HOST
        self.port = settings.MINECRAFT_RCON_PORT
        self.password = settings.MINECRAFT_RCON_PASSWORD

    def execute(self, command: str) -> str:
        if not command.strip():
            raise ValueError("El comando no puede estar vacío")

        if not self.password:
            raise ValueError(
                "MINECRAFT_RCON_PASSWORD no está configurada"
            )

        client = RCONClient(
            self.host,
            port=self.port,
        )

        try:
            authenticated = client.login(self.password)

            if not authenticated:
                raise ConnectionError(
                    "Minecraft rechazó la autenticación RCON"
                )

            response = client.command(command)

            return str(response)

        except (ConnectionError, TimeoutError, OSError) as error:
            raise ConnectionError(
                f"No fue posible comunicarse con Minecraft por RCON: {error}"
            ) from error

        finally:
            client.stop()