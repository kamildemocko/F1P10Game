from pathlib import Path

import msgspec


class CircuitWeekendStructure(msgspec.Struct):
    name: str
    day: str
    month: str
    time: str


class Circuit(msgspec.Struct):
    title: str
    date_span: str
    weekend_structure: list[CircuitWeekendStructure]


class Circuits(msgspec.Struct):
    data: list[Circuit]


def get_circuits(file_path: Path) -> Circuits:
    with file_path.open("rb") as file:
        data = msgspec.json.decode(file.read(), type=Circuits)

    return data
