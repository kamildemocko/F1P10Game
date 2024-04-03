from typing import Callable

import arrow
from nicegui import ui

from f1p10game.uis import types as ui_types
from f1p10game.logic.actions import Actions
from f1p10game.logic import helpers
from f1p10game.main.players import PlayersApp
from f1p10game.main import types as ty


class UiLogic:
    def __init__(self, player_handle: PlayersApp):
        self.player_handle = player_handle
        self.actions_handle = Actions(self.player_handle)

    def _fill_ui_players(
            self,
            players_elements: ui_types.CircuitFormPlayers,
            circuit_name: str,
            player_name: str,
            player_choices: dict[str, ty.PlayerChoice],
            on_confirm: Callable,
            on_edit: Callable,
    ) -> bool:
        """
        Fills main data of form
        :returns: True if main data was filled
        """
        player_form: ui_types.CircuitFormPlayer = players_elements.players[player_name]
        player_form.label.text = player_name

        player_choice_for_circuit = player_choices.get(circuit_name, None)

        player_form.buttons.edit.on("click", lambda x=player_form: on_edit(x))
        player_form.buttons.confirm.on(
            "click", lambda x=player_form, n=player_name, c=circuit_name: on_confirm(
                picked_values=self.get_players_picked_choices(x.pten, x.dnf, n, c))
        )

        if player_choice_for_circuit is None:
            player_form.buttons.edit.disable()
            return False

        player_form.pten.value = player_choice_for_circuit.pten
        player_form.dnf.value = player_choice_for_circuit.dnf
        player_form.buttons.timestamp.text = helpers.humanize_timestamp(player_choice_for_circuit.timestamp)

        player_form.pten.disable()
        player_form.dnf.disable()
        player_form.buttons.confirm.disable()

        return True

    def update_ui_data(
            self,
            all_circuits_elements: ui_types.CircuitsFormStructure,
            players: ty.PlayersStruct,
    ):
        for player_name, player_data in players.data.items():

            for one_circuit_name, one_circuit_elements in all_circuits_elements.circuits.items():
                players_form_filled = self._fill_ui_players(
                    one_circuit_elements.players,
                    one_circuit_name,
                    player_name,
                    player_data.choices,
                    helpers.prep_func_on_confirm(
                        self.actions_handle.on_confirm_button_clicked,
                        players,
                        one_circuit_elements.players.players[player_name],
                    ),
                    self.actions_handle.on_edit_button_clicked
                )
                if not players_form_filled:
                    continue

    @staticmethod
    def get_players_picked_choices(
            pten_button: ui.select,
            dnf_button: ui.select,
            player_name: str,
            circuit_name: str,
    ) -> dict[str, ty.PlayerChoice]:
        """
        Prepares a dictionary with circuit name that holds PlayerChoice
        """
        values = {player_name: ty.PlayerChoice(
            circuit=circuit_name,
            pten=pten_button.value,
            dnf=dnf_button.value,
            timestamp=arrow.utcnow().isoformat()
        )}

        return values