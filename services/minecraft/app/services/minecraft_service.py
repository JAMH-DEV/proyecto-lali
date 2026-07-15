from app.rcon.client import MinecraftRconClient


class MinecraftService:

    def __init__(self):
        self.rcon_client = MinecraftRconClient()

    def _execute(self, command: str) -> str:
        return self.rcon_client.execute(command)

    def list_players(self):
        return self._execute("list")