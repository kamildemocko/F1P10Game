from pathlib import Path

from f1p10game.main import types as ty


class CircuitApp:
    def __init__(self, path: Path):
        self.path = path
        self.data = self._parse_data()

    def _parse_data(self) -> ty.Circuits:
        with self.path.open("rb") as file:
            return ty.Circuits.model_validate_json(file.read())
