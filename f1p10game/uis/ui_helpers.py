from nicegui import ui

from f1p10game.main import types as ty


def init_ui_settings(title: str):
    ui.page_title(title)
    ui.label(title).classes("text-4xl")
    ui.separator()


def init_header(players: ty.PlayersStruct) -> ui.html:
    p = players.data.values()
    sorted(p, key=lambda x: x.points)

    labels = []
    with ui.header() as header:
        header.style("background-color: crimson; color: white;")
        for index, player in enumerate(p, start=1):
            labels.append(f"{index}: {player.name} - {player.points} points")

        label = ui.html(content="&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;".join(labels))

    return label


def update_header(header_element: ui.html, players: ty.PlayersStruct):
    p = players.data.values()
    sorted(p, key=lambda x: x.points)

    labels = []
    for index, player in enumerate(p, start=1):
        labels.append(f"{index}: {player.name} - {player.points} points")

    header_element.content = "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;".join(labels)


def init_footer():
    with ui.footer() as footer:
        footer.style("background-color: crimson; color: white;")
        ui.label(text="2024 Kamil Democko")
        ui.link(text="GitHub", target="https://github.com/kamildemocko")
