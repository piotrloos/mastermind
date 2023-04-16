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

        self._game_intro()
        self._game_loop()
        self._game_outro()

    def _game_intro(self):
        """ Prints intro """

        print(
            f"{self._settings.style.greeting_on}"
            f"###################################\n"
            f"#   Welcome to Mastermind Game!   #\n"
            f"###################################\n"
            f"{self._settings.style.greeting_off}"
        )
        print(
            f"I am CodeMaker and I have prepared "
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
            f"You are CodeBreaker, you don't know my pattern and you have "
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
            "Let's play!"
        )
        print()

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

    def _game_outro(self):
        """ Prints outro """

        if self._game_status == 1:
            print(
                f"You found my solution in "
                f"{self._settings.style.number_on}"
                f"{self._guesses_list.guess_index}"
                f"{self._settings.style.number_off}"
                f" guess{'es' if self._guesses_list.guess_index != 1 else ''}."
            )
        elif self._game_status == 2:
            print(
                "You reached guesses limit. Game over!"
            )
        print(
            f"The solution was {self._solution}."
        )
        print(
            "Thanks for playing!"
        )
