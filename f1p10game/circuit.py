from pathlib import Path

from pydantic import BaseModel, Field


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
    all: list[Circuit] = Field(alias="data")


class CircuitApp:
    def __init__(self, path: Path):
        self.path = path
        self.data = self._parse_data()

    def _parse_data(self) -> Circuits:
        with self.path.open("rb") as file:
            return Circuits.model_validate_json(file.read())
