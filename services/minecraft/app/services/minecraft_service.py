import re

from app.commands.say import build_say_command
from app.commands.time import build_time_command
from app.commands.weather import build_weather_command
from app.rcon.client import MinecraftRconClient
from app.commands.give import build_give_command
from app.commands.clear import build_clear_command
from app.commands.summon import build_summon_command
from app.commands.player import build_player_action_command


class MinecraftService:

    def __init__(self):
        self.rcon_client = MinecraftRconClient()

    def _execute(self, command: str) -> str:
        return self.rcon_client.execute(command)

    def say(self, message: str) -> tuple[str, str]:
        command = build_say_command(message)
        response = self._execute(command)

        return command, response

    def set_weather(self, weather: str) -> tuple[str, str]:
        command = build_weather_command(weather)
        response = self._execute(command)

        return command, response

    def set_time(self, value: str | int) -> tuple[str, str]:
        command = build_time_command(value)
        response = self._execute(command)

        return command, response
    def give_item(
        self,
        player: str,
        item: str,
        quantity: int,
    ) -> tuple[str, str]:
        command = build_give_command(
            player,
            item,
            quantity,
        )
        response = self._execute(command)

        return command, response


    def _parse_players(self, response: str) -> dict:
        pattern = (
            r"There are (\d+) of a max of (\d+) players online:? ?(.*)"
        )

        match = re.match(pattern, response)

        if not match:
            raise ValueError(
                f"No fue posible interpretar la respuesta: {response}"
            )

        online = int(match.group(1))
        maximum = int(match.group(2))

        players = []

        if match.group(3):
            players = [
                player.strip()
                for player in match.group(3).split(",")
                if player.strip()
            ]

        return {
            "online": online,
            "max_players": maximum,
            "players": players,
        }

    def list_players(self) -> dict:
        response = self._execute("list")

        return self._parse_players(response)

    def clear_inventory(
        self,
        player: str,
        item: str | None = None,
        quantity: int | None = None,
    ) -> tuple[str, str]:
        command = build_clear_command(
            player,
            item,
            quantity,
        )
        response = self._execute(command)

        return command, response

    def summon(
        self,
        mob: str,
        player: str | None = None,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        count: int = 1,
    ) -> tuple[list[str], list[str]]:
        command = build_summon_command(
            mob=mob,
            player=player,
            x=x,
            y=y,
            z=z,
        )

        commands = []
        responses = []

        for _ in range(count):
            response = self._execute(command)

            commands.append(command)
            responses.append(response)

        return commands, responses


    def modify_player(
        self,
        player: str,
        action: str,
        value: int | None = None,
        target_player: str | None = None,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
    ) -> tuple[str, str]:
        command = build_player_action_command(
            player=player,
            action=action,
            value=value,
            target_player=target_player,
            x=x,
            y=y,
            z=z,
        )

        response = self._execute(command)

        return command, response