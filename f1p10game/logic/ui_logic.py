from typing import Callable

import arrow
from nicegui import ui

from f1p10game.uis import types as ui_types
from f1p10game.logic.actions import Actions
from f1p10game.logic import helpers
from f1p10game.results.results import ResultsApp
from f1p10game.main.players import PlayersApp
from f1p10game.results.types import Result
from f1p10game.results import results_point_table as result_table
from f1p10game.main import types as ty


class UiLogic:
    def __init__(
            self,
            player_handle: PlayersApp,
            result_handle: ResultsApp,
            ui_elements: ui_types.UiStructure
    ) -> None:
        self.player_handle = player_handle
        self.actions_handle = Actions(self.player_handle)
        self.results_handle: ResultsApp = result_handle
        self.ui_elements: ui_types.UiStructure = ui_elements

    def _fill_ui_form(
            self,
            form: dict[str, ui_types.CircuitFormPlayer],
            circuit_name: str,
            player_name: str,
            player_choices: dict[str, ty.PlayerChoice],
            on_confirm: Callable,
            on_edit: Callable,
            results: list[Result],
    ) -> tuple[bool, ty.PointsTuple]:
        """
        Fills main data of form for a player
        :returns: True if main data was filled and points for pten and dnf
        """
        player_form: ui_types.CircuitFormPlayer = form[player_name]
        player_form.label.text = player_name

        player_choice_for_circuit = player_choices.get(circuit_name, None)

        player_form.buttons.edit.on("click", lambda x=player_form: on_edit(x))
        player_form.buttons.confirm.on(
            "click", lambda x=player_form, n=player_name, c=circuit_name: on_confirm(
                picked_values=self.get_players_picked_choices(x.pten, x.dnf, n, c),
            )
        )

        if player_choice_for_circuit is None:
            player_form.buttons.edit.disable()
            return False, ty.PointsTuple((0, 0))

        # fill ui
        player_form.pten.value = player_choice_for_circuit.pten
        player_form.dnf.value = player_choice_for_circuit.dnf
        player_form.buttons.timestamp.text = helpers.humanize_timestamp(player_choice_for_circuit.timestamp)

        player_form.pten.disable()
        player_form.dnf.disable()
        player_form.buttons.confirm.disable()

        if len(results) == 0:
            return True, ty.PointsTuple(0, 0)

        # points
        player_points: ty.CalculatedPoints = self.calculate_points(results, player_choice_for_circuit)
        player_form.result_label.text = helpers.prep_points_label(
            results,
            player_choice_for_circuit,
            player_points
        )

        return True, ty.PointsTuple((player_points.pten, player_points.dnf))

    @staticmethod
    def calculate_points(results: list[Result], player_choices: ty.PlayerChoice) -> ty.CalculatedPoints:
        """
        Calculates points from player choices
        :returns: dataclass of points for player
        """
        pten_result: Result = [pl for pl in results if pl.driver_name == player_choices.pten][0]
        dnf_result: Result = results[-1] if results[-1].time.lower() == "dnf" else None

        pten_points = result_table.get_points_for_position(
            int(pten_result.position) if pten_result.position.isnumeric() else 0
        )
        pten_pos = int(pten_result.position) if pten_result.position.isnumeric() else 0
        dnf_points = (20
                      if dnf_result is not None
                      and dnf_result.driver_name == player_choices.dnf
                      else 0)

        return ty.CalculatedPoints(pten_points, pten_pos, dnf_points)

    def update_ui_data(self) -> None:
        """
        For each player, fills all UI data, form, buttons, table
        :returns: points for players in dict
        """
        players: ty.PlayersStruct = self.player_handle.get_players()
        points: ty.PlayerPoints = {}

        for player_name, player_data in players.data.items():

            for one_circuit_name, one_circuit_elements in self.ui_elements.circuits.items():
                results_for_circuit: list[Result] | None = self.results_handle.get_result_for_circuit(one_circuit_name)

                # race form
                race_form_filled, (pten_points, dnf_points) = self._fill_ui_form(
                    form=one_circuit_elements.race,
                    circuit_name=one_circuit_name,
                    player_name=player_name,
                    player_choices=player_data.choices_race,
                    on_confirm=helpers.prep_func_on_confirm(
                        self.actions_handle.on_confirm_button_clicked,
                        players,
                        one_circuit_elements.race[player_name],
                        "race",
                        self.update_ui_data,
                    ),
                    on_edit=self.actions_handle.on_edit_button_clicked,
                    results=results_for_circuit,
                )

                points[player_name] = points.get(player_name, 0) + pten_points + dnf_points

                if one_circuit_elements.sprint is None:
                    """no sprint this weekend"""
                    continue

                # sprit form
                sprint_form_filled, (pten_points_sprint, dnf_points_sprint) = self._fill_ui_form(
                    form=one_circuit_elements.sprint,
                    circuit_name=one_circuit_name,
                    player_name=player_name,
                    player_choices=player_data.choices_sprint,
                    on_confirm=helpers.prep_func_on_confirm(
                        self.actions_handle.on_confirm_button_clicked,
                        players,
                        one_circuit_elements.sprint[player_name],
                        "sprint",
                        self.update_ui_data,
                    ),
                    on_edit=self.actions_handle.on_edit_button_clicked,
                    results=results_for_circuit,
                )

                if not sprint_form_filled:
                    """sprint form not filled"""
                    continue

                points[player_name] = points.get(player_name, 0) + pten_points_sprint + dnf_points_sprint

        self.update_players_points(points)

    @staticmethod
    def get_players_picked_choices(
            pten_button: ui.select,
            dnf_button: ui.select,
            player_name: str,
            circuit_name: str,
    ) -> dict[str, ty.PlayerChoice]:
        """
        Prepares a dictionary with circuit name that holds PlayerChoice
        :returns: dictionary of player's choice
        """
        values = {player_name: ty.PlayerChoice(
            circuit=circuit_name,
            pten=pten_button.value,
            dnf=dnf_button.value,
            timestamp=arrow.utcnow().isoformat()
        )}

        return values

    def update_players_points(self, points: dict[str, int]) -> None:
        """
        Updates header with provided points
        """
        sorted(points.values())

        labels = []
        for index, (key, val) in enumerate(points.items(), start=1):
            labels.append(f"{index}: {key} - {val} points")

        self.ui_elements.header.content = "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;".join(labels)
