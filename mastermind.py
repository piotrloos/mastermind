########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main Mastermind base class file      #
#             Piotr Loos (c) 2019-2021 #
########################################

from abc import ABCMeta, abstractmethod
from settings import Settings


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

        self._turns = self._settings.Turns()  # initialize list of turns
        self._solution = None  # initialize solution field
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution

        self._solver = self._settings.solvers[self._settings.solver_index](  # instantiate Solver class
            self._settings,
            self._turns,
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
