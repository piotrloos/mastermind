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
            *_,
    ):
        """ (Solver2) Initializes `MastermindSolver2` class object """

        self._settings = settings

        self._solving_time = 0

        if self._settings.pre_build_patterns:
            self._possible_solutions_list = self._settings.all_patterns_list.copy()  # get list for filtering (copy)
        else:
            # prepare `all_patterns` list/generator for iteration
            if self._settings.use_itertools:
                all_patterns = iter(self._settings.all_patterns_gen)  # init `itertools.product` generator
            else:
                all_patterns = self._settings.all_patterns_gen()  # init my generator

            with Progress(
                items_number=self._settings.patterns_number,
                title="[Solver2] Building list of all patterns from patterns generator...",
                timing=self._settings.progress_timing,
            ) as progress:

                # build list from generator (once per game)
                self._possible_solutions_list = [
                    progress.item(pattern)
                    for pattern in all_patterns
                ]

        self._get_solution()

    def _get_solution(self):
        """ (Solver2) Gets and saves one possible solution from the list """

        self._possible_solutions_number = len(self._possible_solutions_list)

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
    def solving_time(self):
        """ (Solver2) Returns total solving time """

        return self._solving_time

    def update_solving_time(self, exe_time):
        """ (Solver2) Updates execution time by the Progress instance """

        self._solving_time += exe_time  # Solver2 accumulates solving time from several Progress instances per game

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
            self._possible_solutions_list = [
                possible_solution
                for possible_solution in self._possible_solutions_list
                if progress.item(
                    turn.pattern.calculate_black_pegs(possible_solution) == turn.response.black_pegs
                    and
                    turn.pattern.calculate_black_white_pegs(possible_solution) == turn.response.black_white_pegs
                )
            ]

        self._get_solution()

        print(
            f"[Solver2] Number of possible solutions is now "
            f"{self._possible_solutions_number:,} of {patterns_old_number:,} "
            f"(rejected {100 * (1 - self._possible_solutions_number / patterns_old_number):.2f}% of patterns)."
        )

        if self._possible_solutions_number == 1:
            print(
                f"[Solver2] Now I know that {self._current_possible_solution} is the only possible solution!"
            )

        return self._current_possible_solution
