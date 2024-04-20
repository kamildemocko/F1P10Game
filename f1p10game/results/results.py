from pathlib import Path

from f1p10game.results.types import Result, Results, ThisCircuitResults


class ResultsApp:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = self._parse_data()

    def _parse_data(self) -> Results:
        with self.path.open("rb") as file:
            return Results.model_validate_json(file.read())

    def get_result_for_circuit(self, circuit_name: str) -> ThisCircuitResults | None:
        """
        Filters result from one track
        :returns: list of Result type (should be sorted when scrapped)
        """
        search_circuit: str = circuit_name.lower()
        case_lower_data_sprint: dict[str, list[Result]] = {k.lower(): v for k, v in self.data.sprint.items()}
        case_lower_data_race: dict[str, list[Result]] = {k.lower(): v for k, v in self.data.race.items()}

        this_circuit: ThisCircuitResults | None = ThisCircuitResults(
            case_lower_data_sprint.get(search_circuit),
            case_lower_data_race.get(search_circuit),
        )

        return this_circuit
