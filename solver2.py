########################################
# My version of famous game Mastermind #
# solver2.py                           #
# Mastermind Solver2                   #
#             Piotr Loos (c) 2019-2020 #
########################################

from tools import Progress
from random import randrange


class MastermindSolver2:
    """ Contains Mastermind Solver2 (patterns list filtering Solver) """

    def __init__(
            self,
            settings,
            turns,
    ):
        """ (Solver2) Initializes `MastermindSolver2` class object """

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns

        self._solving_time = 0

        self._possible_solutions_list = self._settings.all_patterns_list.copy()  # get list of all possible solutions
        self._analyze_the_list()

    def _analyze_the_list(self):
        """ (Solver2) Gets the possible solution, gets the possible solutions number and sets the flag """

        self._possible_solutions_number = len(self._possible_solutions_list)
        self._single_solution_flag = (self._possible_solutions_number == 1)

        if self._possible_solutions_number:
            if self._settings.solver2_random_pattern:
                index = randrange(self._possible_solutions_number)
            else:
                index = 0
            self._current_possible_solution = self._possible_solutions_list[index]
        else:
            self._current_possible_solution = None

    @property
    def possible_solutions_number(self):
        """ (Solver2) Returns number of possible solutions """

        return self._possible_solutions_number

    @property
    def current_possible_solution(self):
        """ (Solver2) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def single_solution_flag(self):
        """ (Solver2) Returns single possible solution flag """

        return self._single_solution_flag

    @property
    def solving_time(self):
        """ (Solver2) Returns total solving time """

        return self._solving_time

    def update_solving_time(self, exe_time):
        """ (Solver2) Updates execution time by the Progress instance """

        self._solving_time += exe_time

    def check_possible_solution(self, possible_solution):
        """ (Solver2) Checks if given possible solution can be a solution based on all previous turns """

        return possible_solution in self._possible_solutions_list

    def calculate_possible_solution(self, turn, *_):
        """ (Solver2) Calculates the next possible solution after current turn """

        patterns_old_number = self._possible_solutions_number

        with Progress(
            items_number=patterns_old_number,
            title="[Solver2] Filtering patterns list...",
            timing=self._settings.progress_timing,
            update_time_func=self.update_solving_time,
        ) as progress:

            # TODO: try to speed up these calculations
            self._possible_solutions_list = self._settings.Patterns(lst=[
                possible_solution
                for possible_solution in self._possible_solutions_list
                if progress.item(
                    turn.pattern.calculate_black_pegs(possible_solution) == turn.response.black_pegs
                    and
                    turn.pattern.calculate_black_white_pegs(possible_solution) == turn.response.black_white_pegs
                )
            ])

        self._analyze_the_list()

        patterns_new_number = self._possible_solutions_number
        print(
            f"[Solver2] Number of possible solutions is now {patterns_new_number} of {patterns_old_number} "
            f"(rejected {100 * (1 - patterns_new_number / patterns_old_number):.2f}% of patterns)."
        )

        return self._current_possible_solution
