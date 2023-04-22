############################################
# My version of the famous Mastermind game #
# mode_helper.py                           #
# Mastermind Helper mode                   #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_mastermind import Mastermind


class MastermindHelper(Mastermind):
    """ Contains Mastermind Helper mode, inherits from Mastermind class """

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        """ Initializes `MastermindHelper` class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        self._mode = "helper"

        class HelperStrings:
            greeting = "Welcome to Mastermind Helper!"
            codemaker_be = "Somebody is"
            codemaker_have = "he has"
            codemaker_adjective = "his"
            codebreaker_be = "You are"
            codebreaker = "you"
            codebreaker_helper = "I"
            codebreaker_verb = "help you guess"

        self._strings = HelperStrings

        self._intro()
        self._loop()
        self._outro()

    # TODO: refactor with Solver's `_take_turn`
    def _take_turn(self, user_input, computer_pattern=None, computer_response=None):
        """ Takes a turn in Helper mode (with `pattern` and `response` from user) """

        if self._game_status != 0:
            raise PermissionError(
                f"{self._settings.style.error_on}"
                f"[Helper] Game is ended! You can't take a turn."
                f"{self._settings.style.error_off}"
            )

        if computer_pattern is not None or computer_response is not None:  # computer is playing

            if type(computer_pattern) is not self._settings.Pattern:
                raise RuntimeError(
                    f"{self._settings.style.error_on}"
                    f"[Helper] Given `computer_pattern` is not the Pattern class object!"
                    f"{self._settings.style.error_off}"
                )
            elif type(computer_response) is not self._settings.Response:
                raise RuntimeError(
                    f"{self._settings.style.error_on}"
                    f"[Helper] Given `computer_response` is not the Response class object!"
                    f"{self._settings.style.error_off}"
                )
            else:
                pattern = computer_pattern
                response = computer_response

        else:  # user is playing

            try:
                pattern, response = self._settings.Response.decode_pattern_response(user_input)
            except ValueError:
                raise ValueError(
                    f"{self._settings.style.error_on}"
                    f"[Helper] You gave me incorrect `pattern=response`! Try something like `" +
                    self._settings.Peg.all_pegs_list[1].char * self._settings.pegs_in_pattern +
                    f"=1,0` or just `=1,0`. Enter again."
                    f"{self._settings.style.error_off}"
                )

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

        guess = self._guesses_list.add_guess(pattern, response)

        if self._settings.print_guesses_list:
            self._guesses_list.print_guesses_list()

        # check game end criteria

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_in_pattern and response.white_pegs == 0:
            if self._solver.check_possible_solution(pattern):
                self._solution = pattern  # save current pattern as proper solution
                self._game_status = 1  # solution is found
            else:
                self._game_status = 3  # no possible solution found
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

        # TODO: print this before guess - temporary disabled
        # print(
        #     f"[Helper] One of the possible solution is {self._solver.current_possible_solution}."
        # )

        # TODO: print info if it's the same proposition as in previous turn or another (new pattern)
