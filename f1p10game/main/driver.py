from pathlib import Path

from f1p10game.main import types as ty


class DriverApp:
    def __init__(self, path: Path):
        self.path = path
        self.data = self._parse_data()

    def _parse_data(self) -> ty.Drivers:
        with self.path.open("rb") as file:
            return ty.Drivers.model_validate_json(file.read())

    def get_driver_names_for_dropdown(self) -> dict[int, str]:
        data = {driver.number: f"{driver.number}: {driver.name.title()}" for driver in self.data.all}

        data = dict(sorted(data.items(), key=lambda x: x[1].split(" ")[-1].strip()))

        return data
