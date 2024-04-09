from nicegui import ui

from f1p10game.uis import ui_helpers
from f1p10game.uis.types import (
    CircuitFormButtons,
    CircuitFormWeekendTable,
    CircuitFormPlayer,
    CircuitFormPlayers,
    CircuitFormStructure,
    UiStructure,
)
from f1p10game.main import types as ty
from f1p10game.main.players import PlayersApp
from f1p10game.logic import actions


class UiBuilder:
    def __init__(self, title: str, player_handle: PlayersApp) -> None:
        self.player_handle: PlayersApp = player_handle
        self.players: ty.PlayersStruct = self.player_handle.get_players()

        ui_helpers.init_ui_settings(title)

    @staticmethod
    def _build_track_weekend_table(circuit: ty.Circuit) -> CircuitFormWeekendTable:
        """
        Ui for weekend table in one circuit
        :returns: Form of table - elements of table
        """
        return ui.aggrid({
            "defaultColDef": {"flex": 1},
            "columnDefs": [
                {"headerName": "Name", "field": "name"},
                # {"headerName": "Month", "field": "month"},
                {"headerName": "Day", "field": "day"},
                {"headerName": "Time", "field": "time"},
            ],
            "rowData": [
                {"name": s.name, "day": s.day, "time": s.time}
                for s in circuit.weekend_structure[::-1]
            ]
        }).classes("max-h-48")

    @staticmethod
    def _build_form_buttons() -> CircuitFormButtons:
        """
        Ui for buttons under players in one circuit
        :returns: Form of buttons - elements
        """
        with ui.row():
            button_confirm = ui.button(text="Set")
            edit_button = ui.button(text="Edit")

            ui.space()

            filled_timestamp = ui.button(text="- take your pick -").classes("my-auto")
            filled_timestamp.disable()

        return CircuitFormButtons(
            confirm=button_confirm,
            edit=edit_button,
            timestamp=filled_timestamp
        )

    def _build_player_form(
            self,
            event: str,
            driver_options: dict[int, str],
    ) -> CircuitFormPlayers:
        """
        Ui for player form part in one circuit
        :returns: Form of players - elements
        """
        players = self.player_handle.get_players()
        created_players: CircuitFormPlayers = {}

        if event == "Sprint":
            ui.separator().classes("bg-sky-700")

        ui.label(text=event).style("font-size: 130%;").classes("my-auto font-bold")
        ui.separator()
        for player_name, player_data in players.data.items():
            pten_value: int = list(driver_options.keys())[0]
            dnf_value: int = list(driver_options.keys())[0]

            label = ui.label(text="").style("font-size: 120%;").classes("my-auto font-bold")
            with ui.row():
                pten_select = ui.select(driver_options, value=pten_value, label="Position 10").classes("w-auto")
                dnf_select = ui.select(driver_options, value=dnf_value, label="First DNF").classes("w-auto")
            res_label = ui.label(text="").classes("text-sky-700 w-auto")

            form_buttons: CircuitFormButtons = self._build_form_buttons()

            created_players[player_name] = CircuitFormPlayer(
                label=label,
                pten=pten_select,
                dnf=dnf_select,
                buttons=form_buttons,
                result_label=res_label,
            )

            ui.space()

        return created_players

    def build_circuit(
            self,
            circuit: ty.Circuit,
            driver_options: dict[int, str]
    ) -> CircuitFormStructure:
        """
        Builds UI for ONE circuit
        :returns: Structure of the circuit - ui elements
        """
        with ui.expansion(
                circuit.circuit_name.replace("2024", "").replace("FORMULA 1", "").strip(),
                caption=f"{circuit.title} ({circuit.date_span})",
                icon="keyboard_double_arrow_right"
        ) as exp:
            sprint_weekend: bool = len([ci for ci in circuit.weekend_structure if "Sprint" in ci.name]) > 0

            with ui.row().classes("justify-center w-full"):
                with ui.column():
                    form_players_race: CircuitFormPlayers = self._build_player_form(
                        "Race", driver_options
                    )

                    form_players_sprint: CircuitFormPlayers | None = self._build_player_form(
                        "Sprint", driver_options
                    ) if sprint_weekend else None

                    ui.button(text="Close", on_click=exp.close)
                    form_table: CircuitFormWeekendTable = self._build_track_weekend_table(circuit)

            exp.classes("w-full md:max-w-md border-[1px]")

        return CircuitFormStructure(race=form_players_race, sprint=form_players_sprint, table=form_table)

    def build_ui(self, circuits: ty.Circuits, driver_options: dict[int, str]) -> UiStructure:
        """
        Builds all the circuits available one by one
        """
        all_circuits: UiStructure.circuits = {}
        header: ui.html = self.build_header(self.players)

        with ui.row():
            for circuit in circuits.all:
                one_circuit: CircuitFormStructure = self.build_circuit(circuit, driver_options)
                all_circuits[circuit.title] = one_circuit

        self.build_footer()

        return UiStructure(header=header, circuits=all_circuits)

    @staticmethod
    def build_footer() -> None:
        """
        Builds footer of the app
        """
        with ui.footer() as footer:
            footer.style("background-color: crimson; color: white;")
            ui.label(text="2024 Kamil Democko")
            ui.link(text="GitHub", target="https://github.com/kamildemocko").classes("text-white")

    @staticmethod
    def build_header(players: ty.PlayersStruct) -> ui.html:
        """
        Builds header of the app
        :returns: UI HTML element for updating points
        """
        labels = []

        with ui.header() as header:
            header.style("background-color: crimson; color: white;")
            for index, player in enumerate(players.data.values(), start=1):
                labels.append(f"{index}: {player.name} - 0 points")

            label = ui.html(content="&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;".join(labels))

            ui.space()

            dice_link = ui.link(text="Roll a random player").classes("text-white")
            dice_link.on("click", lambda x=dice_link: actions.pick_player_at_random(el=x, players=players))

        return label

