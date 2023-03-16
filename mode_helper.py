############################################
# My version of the famous Mastermind game #
# mode_helper.py                           #
# Mastermind Helper                        #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_mastermind import Mastermind


class MastermindHelper(Mastermind):
    """ Contains Mastermind Helper mode, inherits from Mastermind class """

    # TODO: refactor MastermindGame, MastermindHelper, MastermindSolver into one class

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
            f"{self._settings.color.greeting_on}"
            f"#####################################\n"
            f"#   Welcome to Mastermind Helper!   #\n"
            f"#####################################\n"
            f"{self._settings.color.greeting_off}"
        )
        print(
            f"You are CodeBreaker and somebody has prepared "
            f"{self._settings.color.number_on}"
            f"{self._settings.pegs_number}"
            f"{self._settings.color.number_off}"
            f"-peg pattern using "
            f"{self._settings.color.number_on}"
            f"{self._settings.colors_number}"
            f"{self._settings.color.number_off}"
            f" different colors: "
            f"{self._settings.all_colors_list_formatted}"
            f"."
        )
        print(
            f"I am Helper, I don't know somebody's pattern and I have "
            f"{self._settings.color.number_on}"
            f"{self._settings.turns_limit if self._settings.turns_limit else 'unlimited number of'}"
            f"{self._settings.color.number_off}"
            f" turn{'s' if self._settings.turns_limit != 1 else ''} to help you guess the solution."
        )
        print(
            f"There are "
            f"{self._settings.color.number_on}"
            f"{self._settings.patterns_number:,}"  # divide number by comma every 3 digits
            f"{self._settings.color.number_off}"
            f" possible patterns in this game. "
            f"Example pattern is {self._settings.Pattern.get_random_pattern()}."
        )
        print()
        print(
            f"Settings:"
        )
        print(
            f"chosen_solver = "
            f"{self._settings.color.setting_value_on}"
            f"{self._settings.chosen_solver}"
            f"{self._settings.color.setting_value_off}"
        )
        print(
            f"shuffle_colors_before_build = "
            f"{self._settings.color.setting_value_on}"
            f"{self._settings.shuffle_colors_before_build}"
            f"{self._settings.color.setting_value_off}"
        )
        print(
            f"shuffle_colors_during_build = "
            f"{self._settings.color.setting_value_on}"
            f"{self._settings.shuffle_colors_during_build}"
            f"{self._settings.color.setting_value_off}"
        )
        print(
            f"shuffle_patterns_after_build = "
            f"{self._settings.color.setting_value_on}"
            f"{self._settings.shuffle_patterns_after_build}"
            f"{self._settings.color.setting_value_off}"
        )
        print(
            f"solver1_calc_2nd_solution = "
            f"{self._settings.color.setting_value_on}"
            f"{self._settings.solver1_calc_2nd_solution}"
            f"{self._settings.color.setting_value_off}"
        )
        print(
            f"solver2_take_random_pattern = "
            f"{self._settings.color.setting_value_on}"
            f"{self._settings.solver2_take_random_pattern}"
            f"{self._settings.color.setting_value_off}"
        )
        print(
            f"solver2_print_possible_solutions_threshold = "
            f"{self._settings.color.setting_value_on}"
            f"{self._settings.solver2_print_possible_solutions_threshold}"
            f"{self._settings.color.setting_value_off}"
        )
        print()
        print(
            "Let's play!"
        )
        print()

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
            f"{self._settings.color.number_on}"
            f"{self._turns_list.turns_index + 1:>3d}."  # formatted as minimum 3 chars (spaces before number)
            f"{self._settings.color.number_off}"
            f" Enter pattern=response (empty pattern means {self._solver.current_possible_solution}): "
        )

    # TODO: refactor with `solver_take_turn`
    def _helper_take_turn(self, pattern_response_string, pattern=None, response=None):
        """ Takes turn in Helper mode (with `pattern` and `response` from human) """

        if self._game_status != 0:
            raise PermissionError(
                f"{self._settings.color.error_on}"
                f"[Helper] Game is ended! You can't take turn."
                f"{self._settings.color.error_off}"
            )

        if pattern is None or response is None:
            pattern, response = self._settings.Response.decode_pattern_response(pattern_response_string)
            if pattern is None:
                pattern = self._solver.current_possible_solution  # get `pattern` if user enters "=response" only
                # TODO: bug! incorrect pattern -> current_pattern (instead of printing error)
            if response is None:
                raise ValueError(
                    f"{self._settings.color.error_on}"
                    f"[Helper] You gave me incorrect pattern=response! Enter again."
                    f"{self._settings.color.error_off}"
                )
            # TODO: suggest the user example pattern=response to enter
            if pattern is None:
                pattern = self._solver.current_possible_solution  # get `pattern` if user enters "=response" only

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

        turn = self._turns_list.add_turn(pattern, response)

        if self._settings.print_turns_list:
            self._turns_list.print_turns_list()

        # check game end criteria

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            if self._solver.check_possible_solution(pattern):
                self._solution = pattern  # save current pattern as proper solution
                self._game_status = 1  # solution is found
            else:
                self._game_status = 3  # no possible solution found
            return

        # check if the CodeBreaker reached turns limit
        if self._settings.turns_limit and self._turns_list.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

        # try to find the next possible solution
        # TODO: extract running calc function
        if self._solver.calculate_possible_solution(turn) is None:
            self._game_status = 3  # no possible solution found
            return

        # otherwise game is still active

        # TODO: print this before turn - temporary disabled
        # print(
        #     f"[Helper] One of the possible solution is {self._solver.current_possible_solution}."
        # )

        # TODO: print info if it's the same proposition as in previous turn or another (new pattern)

    def _helper_outro(self):
        """ Prints outro """

        if self._game_status == 1:
            print(
                f"The solution is {self._solution}."
            )
            print(
                f"I found somebody's solution for you in "
                f"{self._settings.color.number_on}"
                f"{self._turns_list.turns_index}"
                f"{self._settings.color.number_off}"
                f" turn{'s' if self._turns_list.turns_index != 1 else ''}."
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
                f"Total solving time: "
                f"{self._settings.color.time_on}"
                f"{self._solving_time:.3f}s"
                f"{self._settings.color.time_off}"
                f"."
            )

        print(
            "Thanks for playing!"
        )
