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
from f1p10game.main import types as ty


class UiBuilder:
    def __init__(self, title: str, players: ty.PlayersStruct):
        ui_helpers.init_ui_settings(title)
        self.header = ui_helpers.init_header(players)
        ui_helpers.init_footer()

    @staticmethod
    def _build_track_weekend_table(circuit: ty.Circuit) -> CircuitFormWeekendTable:
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
            event: str,
            players: ty.PlayersStruct,
            driver_options: dict[int, str],
    ) -> CircuitFormPlayers:
        """
        Ui for players in one circuit
        """
        created_players: CircuitFormPlayers = {}

        with ui.card().classes("border-[1px] gap-y-3 w-full"):
            ui.label(text=event)
            ui.separator()
            for player_name, player_data in players.data.items():
                pten_value: int = list(driver_options.keys())[0]
                dnf_value: int = list(driver_options.keys())[0]

                label = ui.label(text="").style("font-size: 120%;").classes("my-auto font-bold")
                with ui.row():
                    pten_select = ui.select(driver_options, value=pten_value, label="Position 10")
                    dnf_select = ui.select(driver_options, value=dnf_value, label="First DNF")

                form_buttons: CircuitFormButtons = self._build_form_buttons()

                created_players[player_name] = CircuitFormPlayer(
                    label=label,
                    pten=pten_select,
                    dnf=dnf_select,
                    buttons=form_buttons,
                )

                ui.space()

        return created_players

    def build_circuit(
            self,
            players: ty.PlayersStruct,
            circuit: ty.Circuit,
            driver_options: dict[int, str]
    ) -> CircuitFormStructure:
        """
        Builds UI for one circuit
        """
        with ui.expansion(circuit.title, caption=circuit.date_span, icon="keyboard_double_arrow_right") as exp:
            sprint_weekend: bool = len([ci for ci in circuit.weekend_structure if "Sprint" in ci.name]) > 0

            form_players_race: CircuitFormPlayers = self._build_player_form(
                "Race", players, driver_options
            )

            form_players_sprint: CircuitFormPlayers | None = self._build_player_form(
                "Sprint", players, driver_options
            ) if sprint_weekend else None

            ui.button(text="Close", on_click=exp.close)
            form_table: CircuitFormWeekendTable = self._build_track_weekend_table(circuit)

        exp.style("width: 412px")

        return CircuitFormStructure(race=form_players_race, sprint=form_players_sprint, table=form_table)

    def build_all_circuits(
            self,
            players: ty.PlayersStruct,
            circuits: ty.Circuits,
            driver_options: dict[int, str]
    ) -> CircuitsFormStructure:
        all_circuits: CircuitsFormStructure = {}

        with ui.row():
            for circuit in circuits.all:
                one_circuit: CircuitFormStructure = self.build_circuit(players, circuit, driver_options)
                all_circuits[circuit.title] = one_circuit

        return all_circuits

    def update_header(self, players: ty.PlayersStruct):
        """
        Updates header with provided main data
        """
        ui_helpers.update_header(self.header, players)
