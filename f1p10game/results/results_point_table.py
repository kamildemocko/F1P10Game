from pathlib import Path

from f1p10game.results.types import PTable


class PointsTable:
    def __init__(self, path: Path):
        self.path = path
        self.race: dict[int, int]
        self.sprint: dict[int, int]

        self._load_data()

    def _load_data(self):
        with self.path.open("rb") as file:
            data = PTable.model_validate_json(file.read())

        self.race = data.race
        self.sprint = data.sprint

    def get_points_for_position(self, position: int, sprint: bool = False) -> int:
        if position < 1 or position > 20:
            return 0

        if sprint:
            return self.sprint[position]
        else:
            return self.race[position]
