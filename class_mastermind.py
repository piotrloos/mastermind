############################################
# My version of the famous Mastermind game #
# class_mastermind.py                      #
# Main Mastermind base class file          #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from abc import ABCMeta, abstractmethod
from class_settings import Settings


class Mastermind(metaclass=ABCMeta):
    """ Contains whole game, base class for MastermindGame and MastermindSolver classes """

    @abstractmethod
    def __init__(
            self,
            *args,
            settings=None,
            **kwargs,
    ):
        """ Initializes new game with given settings """

        if isinstance(settings, Settings):
            self._settings = settings
        else:
            self._settings = Settings(*args, **kwargs)

        self._turns_list = self._settings.TurnsList()  # initialize list of turns
        self._solution = None  # initialize solution field
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution

        self._solver = self._settings.solvers[self._settings.chosen_solver](  # instantiate Solver class
            self._settings,
            self._turns_list,
        )

    @property
    def solution(self):
        """ Returns solution pattern (only when game is ended) """

        if self._game_status == 0:
            raise PermissionError(
                f"{self._settings.color.error_on}"
                f"[Mastermind] No access to the solution when game is active!"
                f"{self._settings.color.error_off}"
            )
        else:
            if self._solution is None:
                raise ValueError(
                    f"{self._settings.color.error_on}"
                    f"[Mastermind] No saved solution in this game!"
                    f"{self._settings.color.error_off}"
                )
            else:
                return self._solution
