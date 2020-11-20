########################################
# My version of famous game Mastermind #
# helper.py                            #
# Mastermind Helper                    #
#             Piotr Loos (c) 2019-2020 #
########################################

from solver import Mastermind


class MastermindHelper(Mastermind):
    """ Contains Mastermind Helper mode, inherits from Mastermind class """

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        """ Initializes `MastermindHelper` class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        self._helper_intro()
        self._helper_loop()
        self._helper_outro()

    def _helper_intro(self):
        """ Prints intro """

        print(
            """
            #####################################
            #   Welcome to Mastermind Helper!   #
            #####################################
            """
        )

        print(
            f"You are CodeBreaker and somebody has prepared {self._settings.pegs_number}-peg pattern",
            f"using {self._settings.colors_number} different colors: {self._settings.all_colors_list}."
        )

        print(
            f"I am Helper and I have {self._settings.turns_limit if self._settings.turns_limit else 'unlimited'}",
            f"turn{'s' if self._settings.turns_limit != 1 else ''} to help you guess the solution pattern."
        )

        print(
            f"There are {self._settings.patterns_number} possible patterns in this game.",
            f"Example pattern is {self._get_random_pattern()}."
        )

        print(
            f"Settings:\n",
            f"solver_index = {self._settings.solver_index}\n",
            f"shuffle_before = {self._settings.shuffle_before}\n",
            f"shuffle_after = {self._settings.shuffle_after}\n"
        )

    def _helper_loop(self):
        """ Main `Helper` loop """

        while not self._game_status:
            try:
                self._helper_take_turn(input(self._helper_prompt))
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
    def _helper_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            f"{self._turns.turns_index + 1:>3d}. "
            f"Enter `pattern=response` (empty pattern means {self._solver.current_possible_solution}): "
        )

    # TODO: refactor with `solver_take_turn`
    def _helper_take_turn(self, pattern_response_string, pattern=None, response=None):
        """ Takes turn in Helper mode (with `pattern` and `response` from human) """

        if self._game_status != 0:
            raise PermissionError(
                "[Helper] Game is ended! You can't take turn."
            )

        if pattern is None or response is None:
            pattern, response = self._decode_pattern_response(pattern_response_string)
            if pattern is None:
                pattern = self._solver.current_possible_solution  # get `pattern` if user enters "=response" only
            if response is None:
                raise ValueError(
                    "[Helper] Given `pattern=response` is incorrect! Enter again."
                )

        print()
        if self._solver.check_possible_solution(pattern):
            print(
                "[Helper] Nice try. Given pattern could be the solution."
            )
            # TODO: ...and sometimes "was the solution!"
        else:
            print(
                "[Helper] Unfortunately given pattern couldn't be the solution!"
            )

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            if self._solver.check_possible_solution(pattern):
                self._solution = pattern  # save current pattern as proper solution
                self._game_status = 1  # solution is found
            else:
                self._game_status = 3  # no possible solution found
            return

        if self._settings.turns_limit and self._turns.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

        if self._solver.calculate_possible_solution(pattern, response) is None:
            self._game_status = 3  # no possible solution found
            return

        # game is still active

        # TODO: print this before turn
        print(
            f"[Helper] One of the possible solution is {self._solver.current_possible_solution}."
        )
        # TODO: print info if it's the same proposition as in previous turn or another (new pattern)

        # TODO: print this by `solver1` or `solver2`, not here
        if self._solver.single_solution_flag:
            print(
                "[Helper] Now I know there is only one possible solution!"
            )

    def _helper_outro(self):
        """ Prints outro """

        print()

        if self._game_status == 1:
            print(
                f"The solution is {self._solution}."
            )
            print(
                f"We found the solution in {self._turns.turns_index}",
                f" turn{'s' if self._turns.turns_index != 1 else ''}."
            )
        elif self._game_status == 2:
            print(
                "We reached turns limit. Game over!"
            )
        elif self._game_status == 3:
            print(
                "Sorry. No possible solution found!"
            )

        if self._settings.progress_timing:
            print(
                f"Total solving time: {self._solving_time:.3f}s."
            )

        print(
            "Thanks for playing!"
        )
