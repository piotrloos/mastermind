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

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns

        self._generator = self._solution_generator()
        self._current_possible_solution = None
        self._second_possible_solution = None
        self._single_solution_flag = False

        self._solving_time = 0

        self._all_patterns_number = len(self._settings.all_patterns_list)

        # TODO: use Progress as a context manager
        self._progress = Progress(
            items_number=self._all_patterns_number,
            title="",
            timing=self._settings.progress_timing,
            update_time_func=self.update_solving_time,
        )
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
    def single_solution_flag(self):
        """ (Solver1) Returns single possible solution flag """

        return self._single_solution_flag

    @property
    def solving_time(self):
        """ (Solver1) Returns total solving time """

        return self._solving_time

    def update_solving_time(self, exe_time):
        """ (Solver1) Updates execution time by the Progress instance """

        self._solving_time += exe_time

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

        self._single_solution_flag = False  # reset the flag

        if self.check_possible_solution(self._current_possible_solution):
            print(
                "[Solver1] Previously found first possible solution still can be a first solution. Not changed."
            )
        else:
            if self._settings.solver1_second_solution and self.check_possible_solution(self._second_possible_solution):
                print(
                    "[Solver1] Previously found second possible solution still can be a solution. Saved as first."
                )
                self._current_possible_solution = self._second_possible_solution
                self._second_possible_solution = None
            else:
                self._current_possible_solution = self._get_next(
                    "[Solver1] Searching for 1st possible solution..."
                )
                # TODO: ^^ not always `first` (especially when second_solution is off)
                if self._current_possible_solution is None:  # no possible solution
                    self._second_possible_solution = None  # no second possible solution also
                    return self._current_possible_solution  # (=None)

        if self._settings.solver1_second_solution:
            if self.check_possible_solution(self._second_possible_solution):
                print(
                    "[Solver1] Previously found second possible solution still can be a second solution. Not changed."
                )
            else:
                self._second_possible_solution = self._get_next(
                    "[Solver1] Searching for 2nd possible solution..."
                )
                if self._second_possible_solution is None:  # no second possible solution -> only one solution!
                    self._single_solution_flag = True  # set the flag

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

        index = 0

        self._progress.start(
            title=self._progress_title,
        )

        for index, pattern in enumerate(self._settings.all_patterns_list, 1):

            if self._progress.item(self.check_possible_solution(pattern)):  # wrapped the long-taking operation

                self._progress.stop(
                    finish=False,
                    summary=f"Found! It's index is {index} of {self._all_patterns_number} "
                            f"overall ({100 * index / self._all_patterns_number:.2f}%)."
                )
                yield pattern
                self._progress.start(
                    title=self._progress_title,
                )

        # after return the last pattern
        self._progress.stop(
            finish=True,
            summary=f"Finished. Reached index {index} of {self._all_patterns_number} "
                    f"overall ({100 * index / self._all_patterns_number:.2f}%)."
        )

        # ensure `index` reached number of all patterns
        assert index == self._all_patterns_number, "[Solver1] Incorrect pattern index value!"

        # no possible solution
