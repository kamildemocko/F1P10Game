import os

from dotenv import load_dotenv
from nicegui import ui

from f1p10game.mix.config import get_config
from f1p10game.mix.circuit import CircuitApp
from f1p10game.mix.driver import DriverApp
from f1p10game.mix.players import PlayersApp
from f1p10game.results.results import ResultsApp
from f1p10game.mix import types as ty
from f1p10game.uis import types as ui_ty
from f1p10game.uis import ui_builder
from f1p10game.logic.ui_logic import UiLogic
from f1p10game.logic.actions import LoggedIn


class Main:
    def __init__(self):
        self.config = get_config()
        load_dotenv("./.env")

        self.title = self.config.title
        self.drivers_handle = DriverApp(self.config.path_drivers)
        self.circuit_handle = CircuitApp(self.config.path_circuits)
        self.players_handle = PlayersApp(self.config.path_players, self.config.initial_players)
        self.results_handle = ResultsApp(self.config.path_results)

        self.logic_handle: UiLogic | None = None
        self.logged_in = LoggedIn

    def handle_login(self, user_password: str, dialog: ui.dialog, login_button: ui.button):
        if user_password != os.getenv("password"):
            ui.notify("Wrong password", color="negative")
            return

        self.logged_in.logged_in = True
        login_button.disable()
        login_button.text = "Logged in"
        dialog.close()
        ui.notify("Logged in", color="positive")

    def handle_logout(self, login_button: ui.button):
        self.logged_in.logged_in = False
        login_button.enable()
        login_button.text = "Log in"
        ui.notify("Logged out", color="positive")

    def run(self):
        circuits: ty.Circuits = self.circuit_handle.data

        ui_builder_handle = ui_builder.UiBuilder(title=self.title, player_handle=self.players_handle)
        ui_elements: ui_ty.UiStructure = ui_builder_handle.build_ui(
            circuits=circuits,
            driver_options=self.drivers_handle.get_driver_names_for_dropdown(),
            handle_login=self.handle_login,
            handle_logout=self.handle_logout,
        )

        self.logic_handle = UiLogic(
            self.players_handle,
            self.results_handle,
            ui_elements,
            self.config.path_points_table
        )

        self.logic_handle.update_ui_data()

        ui.run(viewport="width=device-width, initial-scale=1", host="localhost", port=8085, reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main = Main()
    main.run()

