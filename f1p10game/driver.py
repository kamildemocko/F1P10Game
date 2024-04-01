from pathlib import Path

from pydantic import BaseModel, Field


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


class DriverApp:
    def __init__(self, path: Path):
        self.path = path
        self.data = self._parse_data()

    def _parse_data(self) -> Drivers:
        with self.path.open("rb") as file:
            return Drivers.model_validate_json(file.read())

    def get_driver_names_as_dict_kshort_vshortname(self) -> dict[int, str]:
        data = {driver.number: f"{driver.number}: {driver.name.title()}" for driver in self.data.all}

        data = dict(sorted(data.items()))

        return data
