from typing import Any, Callable

from players import PlayersStruct, PlayerChoice


class ElementEditUpdater:
    def __init__(self, edit_button: Any):
        self.edit_button = edit_button

    def switch(self, edit_button, elements: list[Any]):

        if edit_button.enabled:
            self.edit_button.disable()
            for element in elements:
                element.enable()
        else:
            edit_button.enable()
            for element in elements:
                element.disable()


class ElementSetUpdater:
    def __init__(self, update_players: Callable):
        self.update_players = update_players

    def set(self, players: PlayersStruct, values: dict[str, PlayerChoice], elements: list[Any]):
        self.update_players(players, values)

        for element in elements:
            element.disable()

        # add edit
        # timestampI
