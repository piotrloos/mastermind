########################################
# My version of famous game Mastermind #
# solver_mode1.py                      #
# Mastermind Solver MODE 1             #
#             Piotr Loos (c) 2019-2020 #
########################################

from solver_mode1_gen import MastermindSolverMode1Generator


class MastermindSolverMode1:
    """ Contains Mastermind Solver MODE 1 (patterns checking generator mode) """

    def __init__(
            self,
            settings,
            turns,
            calculate_black_pegs,
            calculate_black_white_pegs,
    ):
        """ (MODE 1) Initializes `MastermindSolverMode1` class object """

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns
        self._calculate_black_pegs = calculate_black_pegs
        self._calculate_black_white_pegs = calculate_black_white_pegs

        self._generator = MastermindSolverMode1Generator(self._settings, self.check_possible_solution)
        self._current_possible_solution = None
        self._second_possible_solution = None
        self._single_solution_flag = False

        self._time_elapsed = 0

        self.calculate_possible_solution()  # get first possible solution

    @property
    def possible_solutions_number(self):
        """ (MODE 1) Returns number of possible solutions """

        raise NotImplementedError(
            "It is impossible to calculate number of possible solutions in MODE 1!"
        )

    @property
    def current_possible_solution(self):
        """ (MODE 1) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def single_solution_flag(self):
        """ (MODE 1) Returns single possible solution flag """

        return self._single_solution_flag

    @property
    def solving_time(self):
        """ (MODE 1) Returns total solving time """

        return self._generator.solving_time

    def check_possible_solution(self, possible_solution):
        """ (MODE 1) Checks if given possible solution can be a solution based on all previous turns """

        if possible_solution is None:
            return False

        # TODO: try to speed up these calculations
        return all(
            self._calculate_black_pegs(turn.pattern, possible_solution) ==
            turn.response.black_pegs
            and
            self._calculate_black_white_pegs(turn.pattern, possible_solution) ==
            turn.response.black_pegs + turn.response.white_pegs
            for turn in self._turns
        )

    def calculate_possible_solution(self, *_):
        """ (MODE 1) Calculates the next possible solution after current turn """

        # TODO: refactor this method to avoid bug in Progress state (when generator is exhausted)
        # TODO: generator exhausted bug

        self._single_solution_flag = False  # reset the flag

        if self.check_possible_solution(self._current_possible_solution):
            print(
                "[Solver1] Previously found first possible solution still can be a first solution. Not changed."
            )
        else:
            if self._settings.mode1_second_solution and self.check_possible_solution(self._second_possible_solution):
                print(
                    "[Solver1] Previously found second possible solution still can be a solution. Saved as first."
                )
                self._current_possible_solution = self._second_possible_solution
                self._second_possible_solution = None
            else:
                self._current_possible_solution = self._generator.get_next(
                    "[Solver1] Searching for first possible solution..."
                )
                # TODO: ^^ not always `first` (especially when second_solution is off)
                if self._current_possible_solution is None:  # no possible solution
                    self._second_possible_solution = None  # no second possible solution also
                    return self._current_possible_solution  # (=None)

        if self._settings.mode1_second_solution:
            if self.check_possible_solution(self._second_possible_solution):
                print(
                    "[Solver1] Previously found second possible solution still can be a second solution. Not changed."
                )
            else:
                self._second_possible_solution = self._generator.get_next(
                    "[Solver1] Searching for second possible solution..."
                )
                if self._second_possible_solution is None:  # no second possible solution -> only one solution!
                    self._single_solution_flag = True  # set the flag

        return self._current_possible_solution
