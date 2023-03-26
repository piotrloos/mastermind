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
            f"{self._settings.style.greeting_on}"
            f"#####################################\n"
            f"#   Welcome to Mastermind Solver!   #\n"
            f"#####################################\n"
            f"{self._settings.style.greeting_off}"
        )
        print(
            f"You are CodeMaker and you have prepared "
            f"{self._settings.style.number_on}"
            f"{self._settings.pegs_in_pattern}"
            f"{self._settings.style.number_off}"
            f"-peg pattern using "
            f"{self._settings.style.number_on}"
            f"{self._settings.peg_colors}"
            f"{self._settings.style.number_off}"
            f" different colors: "
            f"{self._settings.all_colors_list_formatted}"
            f"."
        )
        print(
            f"I am CodeBreaker, I don't know your pattern and I have "
            f"{self._settings.style.number_on}"
            f"{self._settings.guesses_limit if self._settings.guesses_limit else 'unlimited number of'}"
            f"{self._settings.style.number_off}"
            f" turn{'s' if self._settings.guesses_limit != 1 else ''} to guess the solution."
        )
        print(
            f"There are "
            f"{self._settings.style.number_on}"
            f"{self._settings.patterns_number:,}"  # divide number by comma every 3 digits
            f"{self._settings.style.number_off}"
            f" possible patterns in this game. "
            f"Example pattern is {self._settings.Pattern.get_random_pattern()}."
        )
        print()
        print(
            f"Settings:"
        )
        print(
            f"chosen_solver = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.chosen_solver}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"pre_build_patterns = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.pre_build_patterns}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"use_itertools_for_build = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.use_itertools_for_build}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"shuffle_colors_before_build = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.shuffle_colors_before_build}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"shuffle_colors_during_build = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.shuffle_colors_during_build}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"shuffle_patterns_after_build = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.shuffle_patterns_after_build}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"solver1_calc_2nd_solution = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.solver1_calc_2nd_solution}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"solver2_take_random_pattern = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.solver2_take_random_pattern}"
            f"{self._settings.style.setting_value_off}"
        )
        print(
            f"solver2_print_possible_solutions_threshold = "
            f"{self._settings.style.setting_value_on}"
            f"{self._settings.solver2_print_possible_solutions_threshold}"
            f"{self._settings.style.setting_value_off}"
        )
        print()
        print(
            "Let's play!"
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
        """ Returns styled prompt for `input` function """

        return (
            f"{self._settings.style.number_on}"
            f"{self._guesses_list.guess_index + 1:>3d}."  # formatted as minimum 3 chars (spaces before number)
            f"{self._settings.style.number_off}"
            f" Enter response for pattern {self._solver.current_possible_solution}: "
        )

    # TODO: refactor with `helper_take_turn`
    def _solver_take_turn(self, user_response_string, computer_response=None):
        """ Takes a turn as the CodeBreaker (with `user_response_string` or `computer_response` from CodeMaker) """

        if self._game_status != 0:
            raise PermissionError(
                f"{self._settings.style.error_on}"
                f"[Solver] Game is ended! You can't take a turn."
                f"{self._settings.style.error_off}"
            )

        if computer_response is not None:  # computer is playing

            if type(computer_response) is not self._settings.Response:
                raise RuntimeError(
                    f"{self._settings.style.error_on}"
                    f"[Solver] Given computer response is not the Response class object!"
                    f"{self._settings.style.error_off}"
                )
            else:
                response = computer_response

        else:  # user is playing

            try:
                response = self._settings.Response.decode_response(user_response_string)
            except ValueError:
                raise ValueError(
                    f"{self._settings.style.error_on}"
                    f"[Solver] You gave me incorrect response! Enter again."
                    f"{self._settings.style.error_off}"
                )
            # TODO: suggest the user example response to enter

        pattern = self._solver.current_possible_solution
        print()

        guess = self._guesses_list.add_guess(pattern, response)

        if self._settings.print_guesses_list:
            self._guesses_list.print_guesses_list()

        # check game end criteria

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_in_pattern and response.white_pegs == 0:
            self._solution = pattern  # save current pattern as proper solution
            self._game_status = 1  # solution is found
            return

        # check if the CodeBreaker reached guesses limit
        if self._settings.guesses_limit and self._guesses_list.guess_index >= self._settings.guesses_limit:
            self._game_status = 2  # reached guesses limit
            return

        # try to find the next possible solution
        # TODO: extract running calc function
        if self._solver.calculate_possible_solution(guess) is None:
            self._game_status = 3  # no possible solution found
            return

        # otherwise game is still active

    def _solver_outro(self):
        """ Prints outro """

        if self._game_status == 1:
            print(
                f"The solution is {self._solution}."
            )
            print(
                f"I found your solution in "
                f"{self._settings.style.number_on}"
                f"{self._guesses_list.guess_index}"
                f"{self._settings.style.number_off}"
                f" guess{'es' if self._guesses_list.guess_index != 1 else ''}."
            )
        elif self._game_status == 2:
            print(
                "I reached guesses limit. Game over!"
            )
        elif self._game_status == 3:
            print(
                "Sorry. No possible solution found!"
            )

        if self._settings.progress_timing:
            print(
                f"Total solving time: "
                f"{self._settings.style.time_on}"
                f"{self._solving_time:.3f}s"
                f"{self._settings.style.time_off}"
                f"."
            )

        print(
            "Thanks for playing!"
        )
