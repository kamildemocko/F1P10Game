from pathlib import Path

from pydantic import BaseModel


class CircuitWeekendStructure(BaseModel):
    name: str
    day: str
    month: str
    time: str


class Circuit(BaseModel):
    title: str
    date_span: str
    weekend_structure: list[CircuitWeekendStructure]


class Circuits(BaseModel):
    data: list[Circuit]


def get_circuits(file_path: Path) -> Circuits:
    with file_path.open("rb") as file:
        data = Circuits.model_validate_json(file.read())

    return data
