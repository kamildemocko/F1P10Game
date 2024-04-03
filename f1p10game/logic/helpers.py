from typing import Callable
from functools import partial

from nicegui import ui
import arrow

from f1p10game.uis import types as ui_types
from f1p10game.players import PlayersStruct, PlayerChoice


def humanize_timestamp(timestamp: str | None = None) -> str:
    if timestamp is None:
        return arrow.utcnow().humanize()

    return arrow.get(timestamp).humanize()


def prep_func_on_edit():
    pass


# todo delete
def old_prep_func_on_confirm(
        f: Callable,
        buttons: ui_types.CircuitFormButtons,
        players: PlayersStruct,
        pten_element: ui.select,
        dnf_element: ui.select,
) -> Callable:
    return partial(
        f, buttons=buttons, players=players, pten_select=pten_element, dnf_select=dnf_element,
    )


def prep_func_on_confirm(
        f: Callable,
        players: PlayersStruct,
        player_elements: ui_types.CircuitFormPlayer
) -> Callable:
    return partial(
        f,
        buttons=player_elements.buttons,
        players=players,
        pten_select=player_elements.pten,
        dnf_select=player_elements.dnf,
    )
