from app.rcon.client import MinecraftRconClient
from app.commands.say import build_say_command


class MinecraftService:

    def __init__(self):
        self.rcon_client = MinecraftRconClient()

    def _execute(self, command: str) -> str:
        return self.rcon_client.execute(command)

    def list_players(self):
        return self._execute("list")

    def say(self, message: str) -> tuple[str, str]:
        command = build_say_command(message)
        response = self._execute(command)

        return command, response