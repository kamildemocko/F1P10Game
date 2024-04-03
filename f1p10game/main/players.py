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
                choices={},
                timestamp=arrow.utcnow().isoformat(),
            )

        return PlayersStruct(data=ret)

    async def update_players(self, players: PlayersStruct, values: dict[str, PlayerChoice]):
        """
        Updates json file players, this will receive one dictionary of track
        """
        for name, choices in values.items():
            circuit_name = values[name].circuit
            players.data[name].choices[circuit_name] = values[name]

        self.save_players(players)

