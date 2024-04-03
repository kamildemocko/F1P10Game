from nicegui import ui

from f1p10game.uis import ui_helpers
from f1p10game.uis.types import (
    CircuitFormButtons,
    CircuitFormWeekendTable,
    CircuitFormPlayer,
    CircuitFormPlayers,
    CircuitFormStructure,
    CircuitsFormStructure,
)
from f1p10game.players import PlayersStruct
from f1p10game.circuit import Circuit, Circuits


class UiBuilder:
    def __init__(self, title: str, players: PlayersStruct):
        ui_helpers.init_ui_settings(title)
        self.header = ui_helpers.init_header(players)
        ui_helpers.init_footer()

    @staticmethod
    def _build_track_weekend_table(circuit: Circuit) -> CircuitFormWeekendTable:
        """
        Ui for weekend table in one circuit
        """
        return ui.aggrid({
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

    @staticmethod
    def _build_form_buttons() -> CircuitFormButtons:
        """
        Ui for buttons under players in one circuit
        """
        with ui.row():
            button_confirm = ui.button(text="Set").classes("my-auto")
            edit_button = ui.button(text="Edit").classes("my-auto")

            ui.space()

            filled_timestamp = ui.button(text="-- take your pick --").classes("my-auto")
            filled_timestamp.disable()

        return CircuitFormButtons(
            confirm=button_confirm,
            edit=edit_button,
            timestamp=filled_timestamp
        )

    def _build_player_form(
            self,
            players: PlayersStruct,
            driver_options: dict[int, str],
    ) -> CircuitFormPlayers:
        """
        Ui for players in one circuit
        """
        created_players: CircuitFormPlayers = CircuitFormPlayers(players={})

        for player_name, player_data in players.data.items():
            pten_value: int = list(driver_options.keys())[0]
            dnf_value: int = list(driver_options.keys())[0]

            with ui.row():
                label = ui.label(text="").style("font-size: 130%;").classes("my-auto")
                ui.space()

                pten_select = ui.select(driver_options, value=pten_value, label="Position 10")
                dnf_select = ui.select(driver_options, value=dnf_value, label="First DNF")

            form_buttons: CircuitFormButtons = self._build_form_buttons()

            created_players.players[player_name] = CircuitFormPlayer(
                label=label,
                pten=pten_select,
                dnf=dnf_select,
                buttons=form_buttons,
            )

        return created_players

    def build_circuit(
            self,
            players: PlayersStruct,
            circuit: Circuit,
            driver_options: dict[int, str]
    ) -> CircuitFormStructure:
        """
        Builds UI for one circuit
        """
        with ui.expansion(circuit.title, caption=circuit.date_span, icon="keyboard_double_arrow_right") as exp:
            form_players: CircuitFormPlayers = self._build_player_form(players, driver_options)
            ui.button(text="Close", on_click=exp.close)
            form_table: CircuitFormWeekendTable = self._build_track_weekend_table(circuit)

        exp.style("width: 518px")

        return CircuitFormStructure(players=form_players, table=form_table)

    def build_all_circuits(
            self,
            players: PlayersStruct,
            circuits: Circuits,
            driver_options: dict[int, str]
    ) -> CircuitsFormStructure:
        all_circuits: CircuitsFormStructure = CircuitsFormStructure(circuits={})

        with ui.row():
            for circuit in circuits.all:
                one_circuit: CircuitFormStructure = self.build_circuit(players, circuit, driver_options)
                all_circuits.circuits[circuit.title] = one_circuit

        return all_circuits

    def update_header(self, players: PlayersStruct):
        """
        Updates header with provided player data
        """
        ui_helpers.update_header(self.header, players)
