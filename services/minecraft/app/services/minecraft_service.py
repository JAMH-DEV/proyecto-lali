import re

from app.commands.say import build_say_command
from app.commands.time import build_time_command
from app.commands.weather import build_weather_command
from app.rcon.client import MinecraftRconClient
from app.commands.give import build_give_command
from app.commands.clear import build_clear_command
from app.commands.summon import build_summon_command
from app.commands.player import build_player_action_command
from app.commands.kill import build_kill_command
from app.commands.server import build_server_command


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

    def kill(
        self,
        action: str,
        player: str | None = None,
        mob: str | None = None,
        radius: float | None = None,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        include_players: bool = False,
        confirm: bool = False,
    ) -> tuple[str, str]:
        command = build_kill_command(
            action=action,
            player=player,
            mob=mob,
            radius=radius,
            x=x,
            y=y,
            z=z,
            include_players=include_players,
            confirm=confirm,
        )

        response = self._execute(command)

        return command, response
    
    def manage_server(
        self,
        action: str,
        player: str | None = None,
        reason: str | None = None,
        confirm: bool = False,
    ) -> tuple[str, str]:
        command = build_server_command(
            action=action,
            player=player,
            reason=reason,
            confirm=confirm,
        )

        response = self._execute(command)

        return command, response
    def list_whitelist(self) -> dict:
    response = self._execute("whitelist list")

    return self._parse_name_list(
        response=response,
        empty_phrases={
            "There are no whitelisted players",
            "There are no whitelisted players.",
        },
    )


    def list_banned_players(self) -> dict:
        response = self._execute("banlist players")

        return self._parse_name_list(
            response=response,
            empty_phrases={
                "There are no bans",
                "There are no bans.",
                "There are no banned players",
                "There are no banned players.",
            },
        )


    def list_banned_ips(self) -> dict:
        response = self._execute("banlist ips")

        parsed = self._parse_name_list(
            response=response,
            empty_phrases={
                "There are no bans",
                "There are no bans.",
                "There are no banned IPs",
                "There are no banned IPs.",
            },
        )

        return {
            "count": parsed["count"],
            "ips": parsed["players"],
        }


    def get_server_status(self) -> dict:
        players = self.list_players()

        return {
            "reachable": True,
            "online": players["online"],
            "max_players": players["max_players"],
            "players": players["players"],
        }


    def _parse_name_list(
        self,
        response: str,
        empty_phrases: set[str],
    ) -> dict:
        normalized_response = response.strip()

        if normalized_response in empty_phrases:
            return {
                "count": 0,
                "players": [],
            }

        if ":" in normalized_response:
            names_text = normalized_response.split(":", 1)[1].strip()
        else:
            names_text = normalized_response

        if not names_text:
            return {
                "count": 0,
                "players": [],
            }

        players = [
            name.strip()
            for name in names_text.split(",")
            if name.strip()
        ]

        return {
            "count": len(players),
            "players": players,
        }