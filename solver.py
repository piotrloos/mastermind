########################################
# My version of famous game Mastermind #
# solver.py                            #
# Mastermind Solver                    #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import Mastermind
from solver_mode1 import MastermindSolverMode1
from solver_mode2 import MastermindSolverMode2


class MastermindSolver(Mastermind):
    """ Contains Mastermind Solver mode, inherits from Mastermind class """

    def __init__(
            self,
            *args,
            **kwargs,
            ):
        """ Initializes `MastermindSolver` class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        # TODO: new flag needed: `self._first_turn`

        solvers = {
            1: MastermindSolverMode1,  # patterns checking generator mode
            2: MastermindSolverMode2,  # patterns list filtering mode
        }

        self._solver = solvers[self._settings.solver_mode](
            self._settings,
            self._turns,
            self._calculate_black_pegs,
            self._calculate_black_white_pegs,
        )

        self._solver_intro()
        self._solver_loop()
        self._solver_outro()

    def _solver_intro(self):
        """ Prints intro """

        print(
            """
            #####################################
            #   Welcome to Mastermind Solver!   #
            #####################################
            """
        )

        print(
            "You are CodeMaker and you have prepared {pegs}-peg pattern using {colors} different colors: {list}."
            .format(
                pegs=self._settings.pegs_number,
                colors=self._settings.colors_number,
                list=self._settings.pegs_list,
            )
        )

        print(
            "I am CodeBreaker and I have {turns}"
            .format(
                turns=self._settings.turns_limit if self._settings.turns_limit else "unlimited",
            ),
            "turn" if self._settings.turns_limit == 1 else "turns",
            "to guess the solution pattern."
        )

        print(
            "There are {number} possible patterns in this game. Example pattern is {pattern}."
            .format(
                number=self._settings.patterns_number,
                pattern=self._get_random_pattern(),
            )
        )

        print(
            "Settings: shuffle_before = {shuffle_before}, shuffle_after = {shuffle_after}, solver_mode = {solver_mode}."
            .format(
                shuffle_before=self._settings.shuffle_before,
                shuffle_after=self._settings.shuffle_after,
                solver_mode=self._settings.solver_mode,
            )
        )

        print()

    def _solver_loop(self):
        """ Main `Solver` loop """

        while not self._game_status:
            try:
                self._solver_take_turn(input(self._solver_prompt))
            except ValueError as err:
                print(err)

    @property
    def _possible_solutions_number(self):
        """ Returns number of possible solutions """

        return self._solver.possible_solutions_number

    @property
    def _solving_time(self):
        """ Returns total solving time """

        return self._solver.solving_time

    @property
    def _solver_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{index:>3d}. Enter `response` for pattern {pattern}: "
            .format(
                index=self._turns.turns_index + 1,
                pattern=self._solver.current_possible_solution,
            )
        )

    # TODO: refactor with `helper_take_turn`
    def _solver_take_turn(self, response_string, response=None):
        """ Takes turn as CodeBreaker (with `response` or `response_string` from CodeMaker) """

        if self._game_status != 0:
            raise PermissionError(
                "[Solver] Game is ended! You can't take turn."
            )

        if response is None:
            response = self._decode_response(response_string)
            if response is None:
                raise ValueError(
                    "[Solver] Given `response` is incorrect! Enter again."
                )

        print()
        pattern = self._solver.current_possible_solution

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            self._solution = pattern  # save current pattern as proper solution
            self._game_status = 1  # solution is found
            return

        if self._settings.turns_limit and self._turns.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

        if self._solver.calculate_possible_solution(pattern, response) is None:
            self._game_status = 3  # no possible solution found
            return

        # game is still active

        if self._solver.single_solution_flag:
            print(
                "[Solver] Now I know there is only one possible solution!"
            )

    def _solver_outro(self):
        """ Prints outro """

        print()

        if self._game_status == 1:
            print(
                "The solution is {pattern}."
                .format(
                    pattern=self._solution,
                )
            )
            print(
                "I found the solution in {turns}"
                .format(
                    turns=self._turns.turns_index,
                ),
                "turn." if self._turns.turns_index == 1 else "turns."
            )
        elif self._game_status == 2:
            print(
                "I reached turns limit. Game over!"
            )
        elif self._game_status == 3:
            print(
                "Sorry. No possible solution found!"
            )

        if self._settings.progress_timing:
            print(
                "Total solving time: {time:.3f}s."
                .format(
                    time=self._solving_time,
                ),
            )

        print(
            "Thanks for playing!"
        )
