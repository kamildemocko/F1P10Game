from nicegui import ui


def init_ui_settings(title: str):
    ui.page_title(title)
    ui.label(title).classes("text-4xl")
    ui.separator()
