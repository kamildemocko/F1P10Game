from dataclasses import dataclass

from pydantic import BaseModel, Field


# PLAYER
class PlayerChoice(BaseModel):
    circuit: str
    pten: int
    dnf: int
    timestamp: str


class Player(BaseModel):
    name: str
    choices_race: dict[str, PlayerChoice]
    choices_sprint: dict[str, PlayerChoice]
    timestamp: str


PlayerPoints = dict[str, int]

PointsTuple = tuple[int, int]


@dataclass
class CalculatedPoints:
    pten: int
    dnf: int


class PlayersStruct(BaseModel):
    data: dict[str, Player]


# DRIVER
class Driver(BaseModel):
    name: str
    short: str
    number: int
    team: str
    country: str
    podiums: str
    points: str
    gp_entered: str
    world_championships: str
    highest_race_finish: str
    highest_grid_position: str
    date_of_birth: str
    place_of_birth: str


class Drivers(BaseModel):
    all: list[Driver] = Field(alias="data")


# CIRCUIT
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

