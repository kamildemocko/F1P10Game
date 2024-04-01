from pathlib import Path

import arrow
from pydantic import BaseModel


class PlayerChoice(BaseModel):
    circuit: str
    pten: int
    dnf: int
    timestamp: str


class Player(BaseModel):
    name: str
    points: int
    choices: dict[str, PlayerChoice]
    timestamp: str


class PlayersStruct(BaseModel):
    data: dict[str, Player]


class PlayersApp:
    def __init__(self, path: Path):
        self.path: Path = path

    def get_players(self) -> PlayersStruct:
        if not self.path.exists():
            return PlayersStruct(data={})

        with self.path.open("rb") as file:
            binary = file.read()

        if len(binary) == 0:
            return PlayersStruct(data={})

        return PlayersStruct.model_validate_json(binary)

    def save_players(self, data: PlayersStruct):
        with self.path.open("w") as file:
            file.write(data.model_dump_json(indent=4))

    @staticmethod
    def get_initial_players_obj(names: list[str]) -> PlayersStruct:
        ret = {}
        for name in names:
            ret[name] = Player(
                name=name,
                points=0,
                choices={},
                timestamp=arrow.utcnow().isoformat(),
            )

        return PlayersStruct(data=ret)
