import asyncio

from nicegui import ui

from f1p10game.logic import helpers
from f1p10game.uis import types as ui_types
from f1p10game.main.players import PlayersApp
from f1p10game.main import types as ty


class Actions:
    def __init__(self, players_handle: PlayersApp):
        self.players_handle = players_handle

    @staticmethod
    def on_edit_button_clicked(player_form: ui_types.CircuitFormPlayer) -> None:
        player_form.pten.enable()
        player_form.dnf.enable()
        player_form.buttons.confirm.enable()
        player_form.buttons.edit.disable()

    async def on_confirm_button_clicked(
            self,
            buttons: ui_types.CircuitFormButtons,
            players: ty.PlayersStruct,
            pten_select: ui.select,
            dnf_select: ui.select,
            picked_values: dict[str, ty.PlayerChoice],
            event_type: str,
    ) -> None:
        async def handle_update_players() -> bool:
            """returns true if success"""
            try:
                await self.players_handle.update_players(players, picked_values, event_type)
                return True

            except Exception as exc:
                print(exc)
                buttons.timestamp.text = f"error:{str(exc)[:33]}"
                return False

        buttons.confirm.disable()
        pten_select.disable()
        dnf_select.disable()
        buttons.timestamp.text = "-- Saving --"

        task = asyncio.create_task(handle_update_players())

        if await task:
            buttons.timestamp.text = helpers.humanize_timestamp()
            buttons.edit.enable()

