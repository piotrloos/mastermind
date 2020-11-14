########################################
# My version of famous game Mastermind #
# game.py                              #
# Mastermind Game                      #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import Mastermind, Pattern


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
            self._solution = self._get_random_pattern()
        else:
            if self._validate_pattern(solution):  # TODO: validate Pattern object?
                self._solution = Pattern(solution)
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
            "I am CodeMaker and I have prepared {pegs}-peg pattern using {colors} different colors: {list}."
            .format(
                pegs=self._settings.pegs_number,
                colors=self._settings.colors_number,
                list=self._settings.pegs_list,
            )
        )

        print(
            "You are CodeBreaker and you have {turns}"
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
            "{index:>3d}. Enter `pattern`: "
            .format(
                index=self._turns.turns_index + 1,
            )
        )

    def _game_take_turn(self, pattern_string, pattern=None):
        """ Takes turn as CodeMaker (with `pattern` or `pattern_string` from CodeBreaker) """

        if self._game_status != 0:
            raise PermissionError(
                "[Game] Game is ended! You can't take turn."
            )

        if pattern is None:
            pattern = self._decode_pattern(pattern_string)
            if pattern is None:
                raise ValueError(
                    "[Game] Given `pattern` is incorrect! Enter again."
                )

        response = self._calculate_response(pattern, self._solution)

        print()
        # TODO: use Solver (MODE1) `check_possible_solution` method here
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
                "You found the solution in {turns}"
                .format(
                    turns=self._turns.turns_index,
                ),
                "turn." if self._turns.turns_index == 1 else "turns."
            )
        elif self._game_status == 2:
            print(
                "You reached turns limit. Game over!"
            )

        print(
            "The solution was {pattern}."
            .format(
                pattern=self._solution,
            )
        )

        print(
            "Thanks for playing!"
        )
