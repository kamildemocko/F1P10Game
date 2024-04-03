from nicegui import ui

from f1p10game.logic import helpers
from f1p10game.uis import types as ui_types
from f1p10game.players import PlayersStruct, PlayerChoice, PlayersApp


class Actions:
    def __init__(self, players_handle: PlayersApp):
        self.players_handle = players_handle

    def on_edit_button_clicked(self):
        pass

    def on_confirm_button_clicked(
            self,
            buttons: ui_types.CircuitFormButtons,
            players: PlayersStruct,
            pten_select: ui.select,
            dnf_select: ui.select,
            picked_values: dict[str, PlayerChoice],
    ) -> None:
        buttons.confirm.disable()
        pten_select.disable()
        dnf_select.disable()

        self.players_handle.update_players(players, picked_values)

        buttons.timestamp.text = helpers.humanize_timestamp()
        buttons.edit.enable()
