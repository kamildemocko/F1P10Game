from dataclasses import dataclass

from nicegui import ui


@dataclass
class CircuitFormButtons:
    confirm: ui.button
    edit: ui.button
    timestamp: ui.button


@dataclass
class CircuitFormWeekendTable:
    table: ui.aggrid


@dataclass
class CircuitFormPlayer:
    label: ui.label
    pten: ui.select
    dnf: ui.select
    buttons: CircuitFormButtons


CircuitFormPlayers = dict[str, CircuitFormPlayer]


@dataclass
class CircuitFormStructure:
    race: dict[str, CircuitFormPlayer]
    sprint: dict[str, CircuitFormPlayer] | None
    table: CircuitFormWeekendTable


CircuitsFormStructure = dict[str, CircuitFormStructure]
