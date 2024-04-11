from pathlib import Path

from nicegui import ui

from f1p10game.main.config import get_config
from f1p10game.main.circuit import CircuitApp
from f1p10game.main.driver import DriverApp
from f1p10game.main.players import PlayersApp
from f1p10game.results.results import ResultsApp
from f1p10game.main import types as ty
from f1p10game.uis import types as ui_ty
from uis import ui_builder
from logic.ui_logic import UiLogic


class Main:
    def __init__(self):
        config = get_config()

        self.title = config.title
        self.drivers_handle = DriverApp(config.path_drivers)
        self.circuit_handle = CircuitApp(config.path_circuits)
        self.players_handle = PlayersApp(config.path_players, config.initial_players)
        self.results_handle = ResultsApp(config.path_results)

        self.logic_handle: UiLogic | None = None

    def run(self):
        circuits: ty.Circuits = self.circuit_handle.data

        ui_builder_handle = ui_builder.UiBuilder(title=self.title, player_handle=self.players_handle)

        ui_elements: ui_ty.UiStructure = ui_builder_handle.build_ui(
            circuits=circuits,
            driver_options=self.drivers_handle.get_driver_names_for_dropdown(),
        )

        self.logic_handle = UiLogic(self.players_handle, self.results_handle, ui_elements)
        self.logic_handle.update_ui_data()

        ui.run(viewport="width=device-width, initial-scale=1", port=80)


if __name__ in {"__main__", "__mp_main__"}:
    main = Main()
    main.run()
