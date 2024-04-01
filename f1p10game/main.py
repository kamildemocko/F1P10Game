from typing import Any, Callable
from pathlib import Path
from dataclasses import dataclass
from functools import partial

import arrow
import nicegui.ui
from nicegui import ui
from pydantic import BaseModel

import ui_methods
import ui_updaters
from circuit import CircuitApp, Circuit, Circuits
from driver import DriverApp
from players import PlayersApp, PlayersStruct, PlayerChoice, Player


@dataclass
class UiFields:
    filled_choices: PlayerChoice | None
    pten_select: nicegui.ui.select
    dnf_select: nicegui.ui.select


class Main:
    def __init__(self):
        self.title = "Formula 1 P-10 Game"

        self.circuits_path: Path = Path("./data/circuits.json")
        self.circuit_handle = CircuitApp(self.circuits_path)

        self.initial_players = ["Kamil", "Katka"]
        self.players_path = Path("./data/players.json")
        self.players_handle = PlayersApp(self.players_path)

        self.drivers_path = Path("./data/drivers.json")
        self.drivers_handle = DriverApp(self.drivers_path)

    def update_players(self, players: PlayersStruct, values: dict[str, PlayerChoice]):
        """
        Updates json file players, this will receive one dictionary of track
        """
        for name, choices in values.items():
            circuit_name = values[name].circuit
            players.data[name].choices[circuit_name] = values[name]

        self.players_handle.save_players(players)

    @staticmethod
    def disable_elements(li: list[Any]) -> None:
        for item in li:
            item.disable()

    @staticmethod
    def enable_elements(li: list[Any]) -> None:
        for item in li:
            item.enable()

    @staticmethod
    def get_choice_for_circuit_pten_dnf(
            pten_button: nicegui.ui.select,
            dnf_button: nicegui.ui.select,
            player_name: str,
            circuit_name: str,
    ) -> dict[str, PlayerChoice]:
        """
        Prepares a dictionary with circuit name that holds PlayerChoice
        """
        values = {player_name: PlayerChoice(
            circuit=circuit_name,
            pten=pten_button.value,
            dnf=dnf_button.value,
            timestamp=arrow.utcnow().isoformat()
        )}

        return values

    def add_circuit_data(self, circuit: Circuit, players: PlayersStruct):
        """
        Create one circuit data expansion
        """
        with ui.expansion(circuit.title, caption=circuit.date_span, icon="keyboard_double_arrow_right") as exp:
            driver_options = self.drivers_handle.get_driver_names_as_dict_kshort_vshortname()
            filled_choices_persons: list[str] = []

            # each player has his own row with dropdowns to choose from
            for player, player_data_values in players.data.items():
                def add_fields_for_player(values: Player) -> UiFields:
                    """
                    Adds fields - dropdowns for each player
                    """
                    filled_choices = values.choices.get(circuit.title, None)
                    pten_value: int = list(driver_options.keys())[0] if filled_choices is None else filled_choices.pten
                    dnf_value: int = list(driver_options.keys())[0] if filled_choices is None else filled_choices.dnf

                    ui.label(text=player.title()).style("font-size: 150%;").classes("my-auto")

                    ui.space()

                    pten_select = ui.select(driver_options, value=pten_value, label="Position 10")
                    dnf_select = ui.select(driver_options, value=dnf_value, label="First DNF")

                    ui.space()

                    return UiFields(filled_choices=filled_choices, pten_select=pten_select, dnf_select=dnf_select)

                with ui.row():
                    fields = add_fields_for_player(player_data_values)

                # buttons and timestamp
                with ui.row():
                    def on_confirm_button_clicked(
                            button_confirm: ui.button,
                            button_edit: ui.button,
                            button_timestamp: ui.button,
                            players: PlayersStruct,
                            player: str,
                            circuit: Circuit,
                            pten_select: ui.select,
                            dnf_select: ui.select
                    ):
                        button_confirm.disable()

                        values = self.get_choice_for_circuit_pten_dnf(pten_select, dnf_select, player, circuit.title)
                        self.update_players(players, values)
                        self.disable_elements([pten_select, dnf_select])
                        button_timestamp.text = arrow.utcnow().humanize()

                        button_edit.enable()

                    def on_edit_button_clicked(
                            button_edit: ui.button, buton_set: ui.button, pten_select: ui.select, dnf_select: ui.select
                    ):
                        button_edit.disable()
                        buton_set.enable()
                        self.enable_elements([pten_select, dnf_select])

                    button_confirm = ui.button(text="Set").classes("my-auto")
                    edit_button = ui.button(text="Edit").classes("my-auto")
                    filled_timestamp = ui.button(text="-- take your pick --").classes("my-auto")
                    filled_timestamp.disable()

                    on_confirm_button_clicked_partial = partial(
                        on_confirm_button_clicked,
                        button_confirm=button_confirm,
                        button_edit=edit_button,
                        button_timestamp=filled_timestamp,
                        players=players,
                        player=player,
                        circuit=circuit,
                        pten_select=fields.pten_select,
                        dnf_select=fields.dnf_select
                    )

                    on_edit_button_clicked_partial = partial(
                        on_edit_button_clicked,
                        button_edit=edit_button,
                        buton_set=button_confirm,
                        pten_select=fields.pten_select,
                        dnf_select=fields.dnf_select
                    )

                    button_confirm.on("click", on_confirm_button_clicked_partial)
                    edit_button.on("click", on_edit_button_clicked_partial).classes("my-auto")

                    ui.space()

                    if fields.filled_choices is not None:
                        filled_timestamp.text = arrow.get(fields.filled_choices.timestamp).humanize()

                    if fields.filled_choices is not None:
                        self.disable_elements([fields.pten_select, fields.dnf_select, button_confirm])
                        filled_choices_persons.append(player)

            with ui.row():
                ui.button(text="Close", on_click=exp.close)

            ui.aggrid({
                "defaultColDef": {"flex": 1},
                "columnDefs": [
                    {"headerName": "Name", "field": "name"},
                    {"headerName": "Month", "field": "month"},
                    {"headerName": "Day", "field": "day"},
                    {"headerName": "Time", "field": "time"},
                ],
                "rowData": [
                    {"name": s.name, "month": s.month, "day": s.day, "time": s.time}
                    for s in circuit.weekend_structure[::-1]
                ]
            }).classes("max-h-48")

        exp.style("width: 518px")
        if len(filled_choices_persons) == len(players.data):
            exp.style("border: thick double tomato;")
        else:
            exp.style("border: thick double whitesmoke;")

    def run(self):
        players: PlayersStruct = self.players_handle.get_players()
        if len(players.data) == 0:
            players = self.players_handle.get_initial_players_obj(self.initial_players)

        ui_methods.init_ui_settings(self.title)
        ui_methods.init_header(players)
        ui_methods.init_footer()

        # CIRCUITS
        circuits: Circuits = self.circuit_handle.data

        with ui.row():
            for circuit in circuits.all:
                self.add_circuit_data(circuit, players)

        ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main = Main()
    main.run()
