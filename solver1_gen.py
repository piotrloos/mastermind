########################################
# My version of famous game Mastermind #
# solver1_gen.py                       #
# Mastermind Solver1 Generator         #
#             Piotr Loos (c) 2019-2020 #
########################################

from tools import Progress


class MastermindSolver1Generator:
    """ (Solver1) Contains possible solutions generator for Solver1 """

    def __init__(
            self,
            settings,
            check_possible_solution,
    ):
        """ (Solver1 Generator) Initializes `MastermindSolver1Generator` class object """

        # TODO: temporary given labels
        self._settings = settings
        self._check_possible_solution = check_possible_solution

        self._all_patterns_list = self._settings.all_patterns_list  # get list of all possible solutions to be checked
        self._all_patterns_index = 0  # initialize possible solutions index
        self._all_patterns_number = len(self._all_patterns_list)

        self._exhausted = False
        self._solving_time = 0

        self._progress = Progress(
            items_number=self._all_patterns_number,
            title="",
            timing=self._settings.progress_timing,
        )

    def get_next(self, progress_title):
        """ (Solver1 Generator) Returns the first possible solution based on all previous turns """

        # TODO: generator exhausted bug
        # if self._exhausted:
        #     raise RuntimeError(
        #       "Solver1 Generator is already exhausted!"
        #     )

        self._progress.start(
            title=progress_title,
        )

        while self._all_patterns_index < self._all_patterns_number:  # index is between 0 and `all_patterns_number`-1

            pattern = self._all_patterns_list[self._all_patterns_index]  # get pattern from list
            self._all_patterns_index += 1  # index is now between 1 and `all_patterns_number`

            if self._progress.item(self._check_possible_solution(pattern)):  # wrapped the long-taking operation
                self._solving_time = self._progress.stop(
                    pause=True,
                    summary=f"Found! It's index is {self._all_patterns_index} of {self._all_patterns_number} "
                            f"overall ({100 * self._all_patterns_index / self._all_patterns_number:.2f}%)."
                )
                return pattern

        # after return the last pattern
        self._solving_time = self._progress.stop(
            pause=False,
            summary=f"Finished. Reached index {self._all_patterns_index} of {self._all_patterns_number} "
                    f"overall ({100 * self._all_patterns_index / self._all_patterns_number:.2f}%)."
        )

        # ensure `index` reached number of all patterns
        assert self._all_patterns_index == self._all_patterns_number, "[Solver1] Incorrect pattern index value"

        # no possible solution
        self._exhausted = True
        return None

    @property
    def solving_time(self):
        """ (Solver1 Generator) Returns total solving time """

        return self._solving_time
