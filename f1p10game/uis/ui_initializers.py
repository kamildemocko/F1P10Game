from nicegui import ui

from ..players import PlayersStruct


def init_ui_settings(title: str):
    ui.page_title(title)
    ui.label(title).classes("text-4xl")
    ui.separator()


def init_header(players: PlayersStruct):
    p = players.data.values()
    sorted(p, key=lambda x: x.points)

    with ui.header() as header:
        header.style("background-color: crimson; color: white;")
        for index, player in enumerate(p, start=1):
            ui.label(text=f"P{index}: {player.name} - {player.points} points")


def init_footer():
    with ui.footer() as footer:
        footer.style("background-color: crimson; color: white;")
        ui.label(text="2024 Kamil Democko")
        ui.link(text="GitHub", target="https://github.com/kamildemocko")
