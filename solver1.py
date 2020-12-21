########################################
# My version of famous game Mastermind #
# solver1.py                           #
# Mastermind Solver1                   #
#             Piotr Loos (c) 2019-2020 #
########################################

from tools import Progress


class MastermindSolver1:
    """ Contains Mastermind Solver1 (patterns checking generator Solver) """

    def __init__(
            self,
            settings,
            turns,
    ):
        """ (Solver1) Initializes `MastermindSolver1` class object """

        self._settings = settings
        self._turns = turns

        self._solving_time = 0

        # prepare `all_patterns` list/generator for iteration
        if self._settings.pre_build_patterns:
            self._all_patterns = self._settings.all_patterns_list  # get list (reference)
        else:
            if self._settings.use_itertools:
                self._all_patterns = iter(self._settings.all_patterns_gen)  # init `itertools.product` generator
            else:
                self._all_patterns = self._settings.all_patterns_gen()  # init my generator

        self._generator = self._solution_generator()
        self._current_possible_solution = None
        self._second_possible_solution = None

        self._first = "first " if self._settings.solver1_second_solution else ""

        self._progress_title = ""

        self.calculate_possible_solution()  # get first possible solution

    @property
    def possible_solutions_number(self):
        """ (Solver1) Returns number of possible solutions """

        raise NotImplementedError(
            "It is impossible to calculate number of possible solutions in Solver1!"
        )

    @property
    def current_possible_solution(self):
        """ (Solver1) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def solving_time(self):
        """ (Solver1) Returns total solving time """

        return self._solving_time

    def update_solving_time(self, exe_time):
        """ (Solver1) Updates execution time by the Progress instance """

        self._solving_time = exe_time  # Solver1 overwrites solving time from one Progress instance per game

    def check_possible_solution(self, possible_solution):
        """ (Solver1) Checks if given possible solution can be a solution based on all previous turns """

        if possible_solution is None:  # TODO: after fixing exhausted bug, this `if` should be deleted
            return False

        # TODO: try to speed up these calculations
        return all(
            possible_solution.calculate_black_pegs(turn.pattern) == turn.response.black_pegs
            and
            possible_solution.calculate_black_white_pegs(turn.pattern) == turn.response.black_white_pegs
            for turn in self._turns
        )

    def calculate_possible_solution(self, *_):
        """ (Solver1) Calculates the next possible solution after current turn """

        # TODO: refactor this method to avoid bug in Progress state (when generator is exhausted)
        # TODO: generator exhausted bug

        if self.check_possible_solution(self._current_possible_solution):
            print(
                f"[Solver1] Previously found {self._first}possible solution {self._current_possible_solution} "
                f"still can be a {self._first}solution. Not changed."
            )
        else:
            if self._settings.solver1_second_solution and self.check_possible_solution(self._second_possible_solution):
                print(
                    f"[Solver1] Previously found second possible solution {self._second_possible_solution} "
                    f"still can be a solution. Saved as first."
                )
                self._current_possible_solution = self._second_possible_solution
                self._second_possible_solution = None
            else:
                self._current_possible_solution = self._get_next(
                    f"[Solver1] Searching for {self._first}possible solution..."
                )
                if self._current_possible_solution is None:  # no possible solution
                    self._second_possible_solution = None  # no second possible solution also
                    return self._current_possible_solution  # (=None)

        if self._settings.solver1_second_solution:
            if self.check_possible_solution(self._second_possible_solution):
                print(
                    f"[Solver1] Previously found second possible solution {self._second_possible_solution} "
                    f"still can be a second solution. Not changed."
                )
            else:
                self._second_possible_solution = self._get_next(
                    f"[Solver1] Searching for second possible solution..."
                )
                if self._second_possible_solution is None:  # no second possible solution -> only one solution!
                    print(
                        f"[Solver1] Now I know that {self._current_possible_solution} is the only possible solution!"
                    )

        return self._current_possible_solution

    def _get_next(self, progress_title):
        """ (Solver1) Gets the next possible solution and handles exception from generator """

        self._progress_title = progress_title

        try:
            return next(self._generator)
        except StopIteration:
            return None

    def _solution_generator(self):
        """ (Solver1) Yields possible solution based on all previous turns """

        with Progress(
            items_number=self._settings.patterns_number,
            timing=self._settings.progress_timing,
            update_time_func=self.update_solving_time,
            auto_start_stop=False,
        ) as progress:

            index = 0
            progress.start(
                title=self._progress_title,
            )

            for index, pattern in enumerate(self._all_patterns, 1):

                if progress.item(self.check_possible_solution(pattern)):  # wrapped the long-taking operation

                    progress.stop(
                        finish=False,
                        summary=f"Found! It is {pattern}.\n"
                                f"[Solver1] It's index is {index:,} of {self._settings.patterns_number:,} "
                                f"overall ({100 * index / self._settings.patterns_number:.2f}%)."
                    )
                    yield pattern
                    progress.start(
                        title=self._progress_title,
                    )

            # ensure `index` reached number of all patterns
            assert index == self._settings.patterns_number, "[Solver1] Incorrect pattern index value!"

            # after yield the last pattern
            progress.stop(
                finish=True,
                summary=f"Finished.\n"
                        f"[Solver1] Reached index {index:,} of {self._settings.patterns_number:,} "
                        f"overall ({100 * index / self._settings.patterns_number:.2f}%)."
            )

            # no possible solution
