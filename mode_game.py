############################################
# My version of the famous Mastermind game #
# mode_game.py                             #
# Mastermind Game                          #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_mastermind import Mastermind


class MastermindGame(Mastermind):
    """ Contains Mastermind Game mode, inherits from Mastermind class """

    # TODO: refactor MastermindGame, MastermindHelper, MastermindSolver into one class

    def __init__(
            self,
            *args,
            solution=None,
            **kwargs,
    ):
        """ Initializes `MastermindGame` class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        self._mode = "game"

        class GameStrings:
            greeting = "Welcome to Mastermind Game!"
            codemaker_be = "I am"
            codemaker_have = "I have"
            codemaker_adjective = "my"
            codebreaker_be = "You are"
            codebreaker = "you"
            codebreaker_helper = "you"
            codebreaker_verb = "guess"

        self._strings = GameStrings

        if type(solution) is self._settings.Pattern:
            self._solution = solution
        else:
            if solution is None:
                # get random solution if pattern was not given
                self._solution = self._settings.Pattern.get_random_pattern()
            else:
                try:
                    self._solution = self._settings.Pattern.decode_pattern(solution)
                except ValueError:
                    raise RuntimeError(
                        f"{self._settings.style.error_on}"
                        f"[Game] Given solution pattern is incorrect!"
                        f"{self._settings.style.error_off}"
                    )

        self._intro()
        self._game_loop()
        self._outro()

    def _game_loop(self):
        """ Main `Game` loop """

        while not self._game_status:
            try:
                self._game_take_turn(input(self._game_prompt))
            except ValueError as err:
                print(err)

    @property
    def _game_prompt(self):
        """ Returns styled prompt for `input` function """

        return (
            f"{self._settings.style.number_on}"
            f"{self._guesses_list.guess_index + 1:>3d}."  # formatted as minimum 3 chars (spaces before number)
            f"{self._settings.style.number_off}"
            f" Enter `pattern` (your guess): "
        )

    def _game_take_turn(self, user_pattern_string, computer_pattern=None):
        """ Takes a turn as the CodeMaker (with `user_pattern_string` or `computer_pattern` from CodeBreaker) """

        if self._game_status != 0:
            raise PermissionError(
                f"{self._settings.style.error_on}"
                f"[Game] Game is ended! You can't take a turn."
                f"{self._settings.style.error_off}"
            )

        if computer_pattern is not None:  # computer is playing

            if type(computer_pattern) is not self._settings.Pattern:
                raise RuntimeError(
                    f"{self._settings.style.error_on}"
                    f"[Game] Given `computer_pattern` is not the Pattern class object!"
                    f"{self._settings.style.error_off}"
                )
            else:
                pattern = computer_pattern
                response = pattern.calculate_response(self._solution)

        else:  # user is playing

            try:
                pattern = self._settings.Pattern.decode_pattern(user_pattern_string)
            except ValueError:
                raise ValueError(
                    f"{self._settings.style.error_on}"
                    f"[Game] You gave me incorrect `pattern`! Try something like `" +
                    self._settings.Peg.all_pegs_list[1].char * self._settings.pegs_in_pattern +
                    f"`. Enter again."
                    f"{self._settings.style.error_off}"
                )

            response = pattern.calculate_response(self._solution)
            print(
                f"[Game] Response for your guess is: {response}"
            )
            print()

            # TODO: use Solver1 `check_possible_solution` method here
            #  to print info if given pattern could be the solution (like in Helper)

        self._guesses_list.add_guess(pattern, response)

        if self._settings.print_guesses_list:
            self._guesses_list.print_guesses_list()

        # check game end criteria

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_in_pattern and response.white_pegs == 0:
            self._game_status = 1  # solution is found
            return

        # check if the CodeBreaker reached guesses limit
        if self._settings.guesses_limit and self._guesses_list.guess_index >= self._settings.guesses_limit:
            self._game_status = 2  # reached guesses limit
            return

        # otherwise game is still active
