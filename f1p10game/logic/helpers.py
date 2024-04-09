from typing import Callable
from functools import partial

import arrow

from f1p10game.uis import types as ui_types
from f1p10game.main import types as ty
from f1p10game.results import types as res_types


def humanize_timestamp(timestamp: str | None = None) -> str:
    """
    Returns humanized time ref of time from timestamp
    """
    if timestamp is None:
        return arrow.utcnow().humanize()

    return arrow.get(timestamp).humanize()


def prep_func_on_confirm(
        f: Callable,
        players: ty.PlayersStruct,
        player_elements: ui_types.CircuitFormPlayer,
        event_type: str,
        refresh_ui: Callable,
) -> Callable:
    """
    Uses partial to fill all available arguments for callable used when clicked confirm
    """
    return partial(
        f,
        buttons=player_elements.buttons,
        players=players,
        pten_select=player_elements.pten,
        dnf_select=player_elements.dnf,
        event_type=event_type,
        refresh_ui=refresh_ui,
    )


def prep_points_label(
        results: list[res_types.Result],
        player_choice: ty.PlayerChoice,
        points: ty.CalculatedPoints
) -> str:
    """
    Prepares label in player form under his picks
    :returns: prepared str for label
    """
    pten_driver = [pl.driver_name for pl in results if pl.driver_name == player_choice.pten][0]
    dnf_driver = [pl.driver_name for pl in results if pl.driver_name == player_choice.dnf][0]

    text_prep: list[str] = []
    if points.pten > 0:
        text_prep.append(f"{pten_driver}: {points.pten} pts for position {points.pten_position}")

    if points.dnf > 0:
        text_prep.append(f"{dnf_driver}: {points.dnf} pts for first DNF")

    return ", ". join(text_prep)
