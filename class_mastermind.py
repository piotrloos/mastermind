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
            self._settings = settings  # save `Settings` object as it is
        else:  # also when settings is None
            self._settings = Settings(*args, **kwargs)  # create new `Settings` object with given parameters

        self._settings.print_settings()  # print settings list if enabled (inside function checks)

        self._guesses_list = self._settings.GuessesList()  # initialize new list of guesses
        self._solution = None  # initialize solution field
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached guesses limit, 3:no possible solution

        self._mode = None  # should be overwritten by child class
        self._strings = None  # should be overwritten by child class

        self._solver = self._settings.solver_class(  # instantiate Solver class
            self._settings,
            self._guesses_list,
        )

    def _intro(self):
        """ Prints intro before the current game starts """

        if self._strings is None:
            raise RuntimeError(
                f"{self._settings.style.error_on}"
                f"[Mastermind] No `strings` object defined!"
                f"{self._settings.style.error_off}"
            )

        print(
            f"{self._settings.style.greeting_on}"
            f"####" +
            (f"#" * len(self._strings.greeting)) +
            f"####\n"
            f"#   "
            f"{self._strings.greeting}"
            f"   #\n"
            f"####" +
            (f"#" * len(self._strings.greeting)) +
            f"####\n"
            f"{self._settings.style.greeting_off}"
        )
        print(
            f"{self._strings.codemaker_be} the CodeMaker and {self._strings.codemaker_have} prepared "
            f"{self._settings.style.number_on}"
            f"{self._settings.pegs_in_pattern}"
            f"{self._settings.style.number_off}"
            f"-peg pattern using "
            f"{self._settings.style.number_on}"
            f"{self._settings.peg_colors}"
            f"{self._settings.style.number_off}"
            f" different colors: "
            f"{self._settings.all_colors_list_formatted}"
            f"."
        )
        print(
            f"{self._strings.codebreaker_be} the CodeBreaker, "
            f"{self._strings.codebreaker} don't know {self._strings.codemaker_adjective} pattern "
            f"and {self._strings.codebreaker_helper} have "
            f"{self._settings.style.number_on}"
            f"{self._settings.guesses_limit if self._settings.guesses_limit else 'unlimited number of'}"
            f"{self._settings.style.number_off}"
            f" turn{'s' if self._settings.guesses_limit != 1 else ''} to {self._strings.codebreaker_verb} the solution."
        )
        print(
            f"There are "
            f"{self._settings.style.number_on}"
            f"{self._settings.patterns_number:,}"  # divide number by comma every 3 digits
            f"{self._settings.style.number_off}"
            f" possible patterns in this game. "
            f"Example pattern is {self._settings.Pattern.get_random_pattern()}."
        )
        print()
        print(
            "Let's play!"
        )
        print()

    def _loop(self):
        """ Contains main Mastermind loop """

        while not self._game_status:  # game_status == 0 means game is active
            try:
                self._take_turn(user_input=input(self._prompt))  # ask the user for input and then take a turn
            except ValueError as err:  # catch only wrong input by the user
                print(err)

    @property
    def _prompt(self):
        """ Returns styled prompt for `input` function """

        if self._mode == "game":
            text = f"Enter `pattern` (your guess): "
        elif self._mode == "solver":
            text = f"Enter `response` for pattern {self._solver.current_possible_solution}: "
        elif self._mode == "helper":
            text = f"Enter `pattern=response` (empty pattern means {self._solver.current_possible_solution}): "
        else:
            raise RuntimeError(
                f"{self._settings.style.error_on}"
                f"[Mastermind] Given mode `{self._mode}` is incorrect!"
                f"{self._settings.style.error_off}"
            )

        return (
            f"{self._settings.style.number_on}"
            f"{self._guesses_list.guess_index + 1:>3d}."  # formatted as minimum 3 chars (spaces before number)
            f"{self._settings.style.number_off} {text}"
        )

    def _take_turn(self, user_input, computer_input=None):
        """ Takes a turn (to be overridden by child class) """

        # TODO: refactor common method parts here
        pass

    @property
    def solution(self):
        """ Returns solution pattern (only when game is ended) """

        if self._game_status == 0:
            raise PermissionError(
                f"{self._settings.style.error_on}"
                f"[Mastermind] No access to the solution when game is active!"
                f"{self._settings.style.error_off}"
            )
        else:
            if self._solution is None:
                raise RuntimeError(
                    f"{self._settings.style.error_on}"
                    f"[Mastermind] No saved solution in this game!"
                    f"{self._settings.style.error_off}"
                )
            else:
                return self._solution

    def _outro(self):
        """ Prints outro after the current game ends """

        if self._strings is None:
            raise RuntimeError(
                f"{self._settings.style.error_on}"
                f"[Mastermind] No `strings` object defined!"
                f"{self._settings.style.error_off}"
            )

        if self._game_status == 1:
            print(
                f"Yeah, {self._strings.codebreaker_helper} found {self._strings.codemaker_adjective} solution in "
                f"{self._settings.style.number_on}"
                f"{self._guesses_list.guess_index}"
                f"{self._settings.style.number_off}"
                f" guess{'es' if self._guesses_list.guess_index != 1 else ''}."
            )
            print(
                f"The solution is {self._solution}."
            )
        elif self._game_status == 2:
            print(
                f"Ouch... {self._strings.codebreaker_helper} reached guesses limit. Game over!"
            )
        elif self._game_status == 3:
            print(
                "Sorry. No possible solution found!"
            )

        if self._mode in ("solver", "helper") and self._settings.progress_timing:
            print(
                f"Total computer solving time: "
                f"{self._settings.style.time_on}"
                f"{self._solver.solving_time:.3f}s"
                f"{self._settings.style.time_off}"
                f"."
            )
