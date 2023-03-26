############################################
# My version of the famous Mastermind game #
# class_solver2.py                         #
# Mastermind Solver2                       #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_tools import Progress
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
            if self._settings.use_itertools_for_build:
                all_patterns = iter(self._settings.all_patterns_gen)  # init `itertools.product` generator
            else:
                all_patterns = self._settings.all_patterns_gen()  # init my generator

            with Progress(
                items_number=self._settings.patterns_number,
                style=self._settings.style,
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
            if self._settings.solver2_take_random_pattern:
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
        """ (Solver2) Checks if given possible solution can be a solution based on all previous guesses """

        return possible_solution in self._possible_solutions_list

    def calculate_possible_solution(self, guess, *_):
        """ (Solver2) Calculates the next possible solution after current guess """

        patterns_old_number = self._possible_solutions_number

        with Progress(
            items_number=patterns_old_number,
            style=self._settings.style,
            title="[Solver2] Filtering patterns list...",
            timing=self._settings.progress_timing,
            update_time_func=self.update_solving_time,
        ) as progress:

            # TODO: try to speed up these calculations
            self._possible_solutions_list = [
                possible_solution
                for possible_solution in self._possible_solutions_list
                if progress.item(
                    guess.pattern.calculate_black_pegs(possible_solution) == guess.response.black_pegs
                    and
                    guess.pattern.calculate_black_white_pegs(possible_solution) == guess.response.black_white_pegs
                )
            ]

        self._get_solution()

        print(
            f"[Solver2] Number of possible solutions is now "
            f"{self._settings.style.number_on}"
            f"{self._possible_solutions_number:,}"
            f"{self._settings.style.number_off}"
            f" of "
            f"{self._settings.style.number_on}"
            f"{patterns_old_number:,}"
            f"{self._settings.style.number_off}"
            f" (rejected "
            f"{self._settings.style.number_on}"
            f"{100 * (1 - self._possible_solutions_number / patterns_old_number):.2f}%"
            f"{self._settings.style.number_off}"
            f" of patterns)."
        )

        if 1 <= self._possible_solutions_number <= self._settings.solver2_print_possible_solutions_threshold:
            if self._possible_solutions_number == 1:
                print(
                    f"[Solver2] Now I know pattern {self._current_possible_solution} is the only possible solution!"
                )
            else:
                print(
                    f"[Solver2] Since there are only "
                    f"{self._settings.style.number_on}"
                    f"{self._possible_solutions_number}"
                    f"{self._settings.style.number_off}"
                    f" possible solutions here is a list of them:"
                )
                for pattern in self._possible_solutions_list:
                    print(pattern)

        print()
        return self._current_possible_solution
