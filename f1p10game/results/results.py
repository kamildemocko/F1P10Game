from pathlib import Path

from f1p10game.results.types import Result, Results


class ResultsApp:
    def __init__(self, path: Path):
        self.path = path
        self.data = self._parse_data()

    def _parse_data(self) -> Results:
        with self.path.open("rb") as file:
            return Results.model_validate_json(file.read())

    def get_result_for_circuit(self, circuit_name: str) -> list[Result] | None:
        this_circuit: Result | None = self.data.data.get(circuit_name, None)
        if this_circuit is None:
            return None

        return sorted(this_circuit, key=lambda x: x.position)
