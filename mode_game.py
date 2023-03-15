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
                    f"{self._settings.color.error_on}"
                    f"Incorrect solution pattern."
                    f"{self._settings.color.error_off}"
                )

        self._game_intro()
        self._game_loop()
        self._game_outro()

    def _game_intro(self):
        """ Prints intro """

        print(
            f"{self._settings.color.greeting_on}"
            f"###################################\n"
            f"#   Welcome to Mastermind Game!   #\n"
            f"###################################\n"
            f"{self._settings.color.greeting_off}"
        )
        print(
            f"I am CodeMaker and I have prepared "
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
            f"You are CodeBreaker, you don't know my pattern and you have "
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
            "Let's play!"
        )

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
            f"\n"
            f"{self._settings.color.number_on}"
            f"{self._turns_list.turns_index + 1:>3d}."
            f"{self._settings.color.number_off}"
            f" Enter "
            f"{self._settings.color.attribute_on}"
            f"pattern"
            f"{self._settings.color.attribute_off}"
            f": "
        )

    def _game_take_turn(self, pattern_string, pattern=None):
        """ Takes turn as CodeMaker (with `pattern` or `pattern_string` from CodeBreaker) """

        if self._game_status != 0:
            raise PermissionError(
                f"{self._settings.color.error_on}"
                f"[Game] Game is ended! You can't take turn."
                f"{self._settings.color.error_off}"
            )

        if pattern is None:
            pattern = self._settings.Pattern.decode_pattern(pattern_string)
            if pattern is None:
                raise ValueError(
                    f"{self._settings.color.error_on}"
                    f"[Game] Given "
                    f"{self._settings.color.attribute_on}"
                    f"pattern"
                    f"{self._settings.color.attribute_off}"
                    f" is incorrect! Enter again."
                    f"{self._settings.color.error_off}"
                )

        response = pattern.calculate_response(self._solution)

        print()
        # TODO: use Solver1 `check_possible_solution` method here
        #  to print info if given pattern could be the solution (like in Helper)

        self._turns_list.add_turn(pattern, response)

        if self._settings.print_turns_list:
            self._turns_list.print_turns_list()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            self._game_status = 1  # solution is found
            return

        if self._settings.turns_limit and self._turns_list.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

    def _game_outro(self):
        """ Prints outro """

        print()

        if self._game_status == 1:
            print(
                f"You found my pattern in "
                f"{self._settings.color.number_on}"
                f"{self._turns_list.turns_index}"
                f"{self._settings.color.number_off}"
                f" turn{'s' if self._turns_list.turns_index != 1 else ''}."
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
