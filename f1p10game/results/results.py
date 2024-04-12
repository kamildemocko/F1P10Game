from pathlib import Path

from f1p10game.results.types import Result, Results


class ResultsApp:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = self._parse_data()

    def _parse_data(self) -> Results:
        with self.path.open("rb") as file:
            return Results.model_validate_json(file.read())

    def get_result_for_circuit(self, circuit_name: str) -> list[Result] | None:
        """
        Filters result from one track
        :returns: list of Result type (should be sorted when scrapped)
        """
        search_circuit: str = circuit_name.lower()
        case_lower_data: dict[str, list[Result]] = {k.lower(): v for k, v in self.data.results.items()}
        this_circuit: list[Result] | None = case_lower_data.get(search_circuit)
        if this_circuit is None:
            return None

        return this_circuit
