############################################
# My version of the famous Mastermind game #
# mode_solver.py                           #
# Mastermind Solver                        #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_mastermind import Mastermind


class MastermindSolver(Mastermind):
    """ Contains Mastermind Solver mode, inherits from Mastermind class """

    # TODO: refactor MastermindGame, MastermindHelper, MastermindSolver into one class

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        """ Initializes `MastermindSolver` class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        self._solver_intro()
        self._solver_loop()
        self._solver_outro()

    def _solver_intro(self):
        """ Prints intro """

        print(
            f"{self._settings.color.greeting_on}"
            f"#####################################\n"
            f"#   Welcome to Mastermind Solver!   #\n"
            f"#####################################\n"
            f"{self._settings.color.greeting_off}"
        )
        print(
            f"You are CodeMaker and you have prepared "
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
            f"I am CodeBreaker, I don't know your pattern and I have "
            f"{self._settings.color.number_on}"
            f"{self._settings.turns_limit if self._settings.turns_limit else 'unlimited number of'}"
            f"{self._settings.color.number_off}"
            f" turn{'s' if self._settings.turns_limit != 1 else ''} to guess the solution."
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
            f"\n"
            f"{self._settings.color.number_on}"
            f"{self._turns_list.turns_index + 1:>3d}."
            f"{self._settings.color.number_off}"
            f" Enter "
            f"{self._settings.color.attribute_on}"
            f"response"
            f"{self._settings.color.attribute_off}"
            f" for pattern {self._solver.current_possible_solution}: "
        )

    # TODO: refactor with `helper_take_turn`
    def _solver_take_turn(self, response_string, response=None):
        """ Takes turn as CodeBreaker (with `response` or `response_string` from CodeMaker) """

        if self._game_status != 0:
            raise PermissionError(
                f"{self._settings.color.error_on}"
                f"[Solver] Game is ended! You can't take turn."
                f"{self._settings.color.error_off}"
            )

        if response is None:
            response = self._settings.Response.decode_response(response_string)
            if response is None:
                raise ValueError(
                    f"{self._settings.color.error_on}"
                    f"[Solver] Given "
                    f"{self._settings.color.attribute_on}"
                    f"response"
                    f"{self._settings.color.attribute_off}"
                    f" is incorrect! Enter again."
                    f"{self._settings.color.error_off}"
                )

        print()
        pattern = self._solver.current_possible_solution

        turn = self._turns_list.add_turn(pattern, response)

        if self._settings.print_turns_list:
            self._turns_list.print_turns_list()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            self._solution = pattern  # save current pattern as proper solution
            self._game_status = 1  # solution is found
            return

        if self._settings.turns_limit and self._turns_list.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

        # TODO: extract running calc function
        if self._solver.calculate_possible_solution(turn) is None:
            self._game_status = 3  # no possible solution found
            return

        # game is still active

    def _solver_outro(self):
        """ Prints outro """

        print()

        if self._game_status == 1:
            print(
                f"The solution is {self._solution}."
            )
            print(
                f"I found your pattern in "
                f"{self._settings.color.number_on}"
                f"{self._turns_list.turns_index}"
                f"{self._settings.color.number_off}"
                f" turn{'s' if self._turns_list.turns_index != 1 else ''}."
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
                f"Total solving time: "
                f"{self._settings.color.time_on}"
                f"{self._solving_time:.3f}s"
                f"{self._settings.color.time_off}"
                f"."
            )

        print(
            "Thanks for playing!"
        )
