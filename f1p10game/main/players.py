from pathlib import Path

import arrow

from f1p10game.main.types import PlayerChoice, Player, PlayersStruct


class PlayersApp:
    def __init__(self, path: Path, default_names: list[str] = None) -> None:
        self.path: Path = path
        self.default_names: list[str] = default_names or ["Player1"]

    def get_players(self) -> PlayersStruct:
        if not self.path.exists():
            return self._get_initial_players_obj()

        with self.path.open("rb") as file:
            binary = file.read()

        if len(binary) == 0:
            return self._get_initial_players_obj()

        return PlayersStruct.model_validate_json(binary)

    def save_players(self, data: PlayersStruct) -> None:
        with self.path.open("w") as file:
            file.write(data.model_dump_json(indent=4))

    def _get_initial_players_obj(self) -> PlayersStruct:
        ret = {}
        for name in self.default_names:
            ret[name] = Player(
                name=name,
                points=0,
                choices_race={},
                timestamp=arrow.utcnow().isoformat(),
            )

        return PlayersStruct(data=ret)

    async def update_players(
            self,
            players: PlayersStruct,
            values: dict[str, PlayerChoice],
            event_type: str,
    ) -> None:
        """
        Updates json file players, this will receive one dictionary of track
        """
        for name, choices in values.items():
            circuit_name = values[name].circuit
            if event_type == "race":
                players.data[name].choices_race[circuit_name] = values[name]
            elif event_type == "sprint":
                players.data[name].choices_sprint[circuit_name] = values[name]
            else:
                raise ValueError("wrong event type")

        self.save_players(players)

