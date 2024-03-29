from typing import Any
from pathlib import Path
from dataclasses import dataclass

import msgspec


@dataclass
class Player:
    name: str
    points: int
    choices: dict[str, Any]


class PlayersStruct(msgspec.Struct):
    data: dict[str, Player]


@dataclass
class PlayerChoice:
    circuit: str
    pten: str
    dnf: str


class Players:
    def __init__(self, path: Path):
        self.path: Path = path

    def get_players(self) -> PlayersStruct:
        if not self.path.exists():
            return PlayersStruct([])

        with self.path.open("rb") as file:
            binary = file.read()

        if len(binary) == 0:
            return PlayersStruct([])

        return msgspec.json.decode(binary, type=PlayersStruct)

    def save_players(self, data: PlayersStruct):
        with self.path.open("wb") as file:
            file.write(msgspec.json.encode(data))

    @staticmethod
    def get_initial_players_obj(names: list[str]) -> PlayersStruct:
        ret = {}
        for name in names:
            ret[name] = Player(
                name=name,
                points=0,
                choices={},
            )

        return PlayersStruct(data=ret)
