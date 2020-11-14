########################################
# My version of famous game Mastermind #
# solver_mode2.py                      #
# Mastermind Solver MODE 2             #
#             Piotr Loos (c) 2019-2020 #
########################################

from tools import Progress
from components import PatternsContainer
from random import randrange


class MastermindSolverMode2:
    """ Contains Mastermind Solver MODE 2 (patterns list filtering mode) """

    def __init__(
            self,
            settings,
            turns,
            calculate_black_pegs,
            calculate_black_white_pegs,
            ):
        """ (MODE 2) Initializes `MastermindSolverMode2` class object """

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns
        self._calculate_black_pegs = calculate_black_pegs
        self._calculate_black_white_pegs = calculate_black_white_pegs

        self._solving_time = 0

        # TODO: for first time it's PatternsContainer object, later it's just list
        self._possible_solutions_list = PatternsContainer(self._settings)  # get list of all possible solutions
        self._analyze_the_list()

    def _analyze_the_list(self):
        """ (MODE 2) Gets the possible solution, gets the possible solutions number and sets the flag """

        self._possible_solutions_number = len(self._possible_solutions_list)
        self._single_solution_flag = (self._possible_solutions_number == 1)

        if self._possible_solutions_number:
            if self._settings.mode2_random_pattern:
                index = randrange(self._possible_solutions_number)
            else:
                index = 0
            self._current_possible_solution = self._possible_solutions_list[index]
        else:
            self._current_possible_solution = None

    @property
    def possible_solutions_number(self):
        """ (MODE 2) Returns number of possible solutions """

        return self._possible_solutions_number

    @property
    def current_possible_solution(self):
        """ (MODE 2) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def single_solution_flag(self):
        """ (MODE 2) Returns single possible solution flag """

        return self._single_solution_flag

    @property
    def solving_time(self):
        """ (MODE 2) Returns total solving time """

        return self._solving_time

    def check_possible_solution(self, possible_solution):
        """ (MODE 2) Checks if given possible solution can be a solution based on all previous turns """

        return possible_solution in self._possible_solutions_list

    def calculate_possible_solution(self, turn_pattern, turn_response, *_):
        """ (MODE 2) Calculates the next possible solution after current turn """

        patterns_old_number = self._possible_solutions_number

        progress = Progress(
            items_number=patterns_old_number,
            title="[Solver2] Filtering patterns list...",
            timing=self._settings.progress_timing,
        )

        progress.start()

        # TODO: try to speed up these calculations
        self._possible_solutions_list = [
            possible_solution
            for possible_solution in self._possible_solutions_list
            if progress.item(
                self._calculate_black_pegs(turn_pattern, possible_solution) ==
                turn_response.black_pegs
                and
                self._calculate_black_white_pegs(turn_pattern, possible_solution) ==
                turn_response.black_pegs + turn_response.white_pegs
            )
        ]

        self._solving_time += progress.stop()

        self._analyze_the_list()

        patterns_new_number = self._possible_solutions_number
        print(
            "[Solver2] Number of possible solutions is now {new} of {old} (rejected {percent:.2f}% of patterns)."
            .format(
                new=patterns_new_number,
                old=patterns_old_number,
                percent=100 * (1 - patterns_new_number / patterns_old_number),
            )
        )

        return self._current_possible_solution
