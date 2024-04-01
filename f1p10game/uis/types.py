from dataclasses import dataclass

from nicegui import ui


@dataclass
class CircuitFormButtons:
    confirm: ui.button
    edit: ui.button
    timestamp: ui.button


@dataclass
class CircuitFormWeekendTable():
    table: ui.aggrid


@dataclass
class CircuitFormPlayer:
    label: ui.label
    pten: ui.select
    dnf: ui.select


@dataclass()
class CircuitFormPlayers:
    players: dict[str, CircuitFormPlayer]


@dataclass
class CircuitFormStructure:
    players: CircuitFormPlayers
    buttons: CircuitFormButtons
    table: CircuitFormWeekendTable


@dataclass
class CircuitsFormStructure:
    circuits: list[CircuitFormStructure]
