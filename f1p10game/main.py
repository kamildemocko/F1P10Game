from pathlib import Path

import arrow
from nicegui import ui

import circuit as ci
import players as pl


class Main:
    def __init__(self):
        self.title = "Formula 1 P-10 Game"
        self.circuits_path: Path = Path("./data/circuits.json")
        self.players_path = Path("./data/players.json")
        self.players_handle = pl.Players(self.players_path)
        self.initial_players = ["Kamil", "Katka"]

    def init_ui_settings(self):
        ui.page_title(self.title)
        ui.label(self.title).classes("text-4xl")
        ui.separator()

    @staticmethod
    def init_header(players: pl.PlayersStruct):
        p = players.data.values()
        sorted(p, key=lambda x: x.points)

        with ui.header() as header:
            header.style("background-color: crimson; color: white;")
            for index, player in enumerate(p, start=1):
                ui.label(text=f"P{index}: {player.name} - {player.points} points")

    @staticmethod
    def init_footer():
        with ui.footer() as footer:
            footer.style("background-color: crimson; color: white;")
            ui.label(text="2024 Kamil Democko")
            ui.link(text="GitHub", target="https://github.com/kamildemocko")

    def update_players(self, players: pl.PlayersStruct, values: dict[str, pl.PlayerChoice]):
        for name, choices in values.items():
            circuit_name = values[name].circuit
            players.data[name].choices[circuit_name] = values[name]

        self.players_handle.save_players(players)

    def add_circuit_data(self, circuit: ci.Circuit, players: pl.PlayersStruct):
        with ui.expansion(circuit.title, caption=circuit.date_span, icon="keyboard_double_arrow_right").classes(
                "w-256") as exp:
            exp.style("width: 512px")

            player_choices = {}
            for player in players.data.keys():
                with ui.row():
                    ui.label(text=player.title()).style("font-size: 150%;").classes("my-auto")
                    pten = ui.input("Who will end in P10?")
                    dnf = ui.input("Who will DNF first?")
                    player_choices[player] = pten, dnf

            def get_values() -> dict[str, pl.PlayerChoice]:
                values = {}

                for key, value in player_choices.items():
                    values[key] = pl.PlayerChoice(
                        circuit=circuit.title,
                        pten=value[0].value,
                        dnf=value[1].value,
                        timestamp=arrow.utcnow().isoformat(),
                    )

                return values

            with ui.row():
                ui.button(text="Confirm", on_click=lambda x: self.update_players(players, get_values()))
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

    def run(self):
        players: pl.PlayersStruct = self.players_handle.get_players()
        if len(players.data) == 0:
            players = self.players_handle.get_initial_players_obj(self.initial_players)

        self.init_ui_settings()
        self.init_header(players)
        self.init_footer()

        # CIRCUITS
        circuits: ci.Circuits = ci.get_circuits(self.circuits_path)

        with ui.row():
            for circuit in circuits.data:
                self.add_circuit_data(circuit, players)

        ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main = Main()
    main.run()
