from dataclasses import dataclass

from pydantic import BaseModel


class Result(BaseModel):
    position: str
    driver_number: int
    driver_name: str
    team_name: str
    time: str
    points: str


class Results(BaseModel):
    sprint: dict[str, list[Result]] = dict[str, list[Result]]
    race: dict[str, list[Result]] = dict[str, list[Result]]


class PTable(BaseModel):
    race: dict[int, int]
    sprint: dict[int, int]


@dataclass
class ThisCircuitResults:
    sprint: list[Result]
    race: list[Result]
