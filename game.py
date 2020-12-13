########################################
# My version of famous game Mastermind #
# game.py                              #
# Mastermind Game                      #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import Mastermind


class MastermindGame(Mastermind):
    """ Contains Mastermind Game mode, inherits from Mastermind class """

    def __init__(
            self,
            *args,
            solution=None,  # TODO: give tuple or Pattern object?
            **kwargs,
    ):
        """ Initializes `MastermindGame` class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        if solution is None:  # check if `solution` is given
            self._solution = self._settings.Pattern.get_random_pattern()
        else:
            if self._settings.Pattern.validate_pattern(solution):  # TODO: validate Pattern object?
                self._solution = self._settings.Pattern(solution)
            else:
                raise ValueError(
                    "Incorrect solution pattern."
                )

        self._game_intro()
        self._game_loop()
        self._game_outro()

    def _game_intro(self):
        """ Prints intro """

        print(
            """
            ###################################
            #   Welcome to Mastermind Game!   #
            ###################################
            """
        )

        print(
            f"I am CodeMaker and I have prepared {self._settings.pegs_number}-peg pattern "
            f"using {self._settings.colors_number} different colors: {self._settings.all_colors_list}."
        )

        print(
            f"You are CodeBreaker "
            f"and you have {self._settings.turns_limit if self._settings.turns_limit else 'unlimited'} "
            f"turn{'s' if self._settings.turns_limit != 1 else ''} to guess the solution pattern."
        )

        print(
            f"There are {self._settings.patterns_number:,} possible patterns in this game. "
            f"Example pattern is {self._settings.Pattern.get_random_pattern()}."
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
        """ Returns formatted prompt for `input` function """

        return (
            f"{self._turns.turns_index + 1:>3d}. Enter `pattern`: "
        )

    def _game_take_turn(self, pattern_string, pattern=None):
        """ Takes turn as CodeMaker (with `pattern` or `pattern_string` from CodeBreaker) """

        if self._game_status != 0:
            raise PermissionError(
                "[Game] Game is ended! You can't take turn."
            )

        if pattern is None:
            pattern = self._settings.Pattern.decode_pattern(pattern_string)
            if pattern is None:
                raise ValueError(
                    "[Game] Given `pattern` is incorrect! Enter again."
                )

        response = pattern.calculate_response(self._solution)

        print()
        # TODO: use Solver1 `check_possible_solution` method here
        #  to print info if given pattern could be the solution (like in Helper)

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            self._game_status = 1  # solution is found
            return

        if self._settings.turns_limit and self._turns.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

    def _game_outro(self):
        """ Prints outro """

        print()

        if self._game_status == 1:
            print(
                f"You found the solution in {self._turns.turns_index} "
                f"turn{'s' if self._turns.turns_index != 1 else ''}."
            )
        elif self._game_status == 2:
            print(
                "You reached turns limit. Game over!"
            )

        print(
            f"The solution was {self._solution}."
        )

        print(
            "Thanks for playing!"
        )
