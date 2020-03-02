########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main Mastermind classes file         #
#             Piotr Loos (c) 2019-2020 #
########################################

from abc import abstractmethod
from random import randrange
from settings import *
from tools import Progress, shuffle


class Mastermind:
    """ Contains whole game, base class for MastermindGame and MastermindSolver classes """

    @abstractmethod
    def __init__(self, *args, colors=COLORS, pegs=PEGS, turns_limit=TURNS_LIMIT, **kwargs):
        """ Initializes new game with given settings """

        # check if given `colors` number is correct
        if colors in range(2, 13):  # from 2 to 12
            self._colors_number = colors
        else:
            raise ValueError("Incorrect number of colors.")

        # check if given `pegs` number is correct
        if pegs in range(2, 11):  # from 2 to 10
            self._pegs_number = pegs
        else:
            raise ValueError("Incorrect number of pegs.")

        # check if given `turns_limit` number is correct
        if turns_limit in range(1, 21):  # from 1 to 20
            self._turns_limit = turns_limit
        else:
            raise ValueError("Incorrect number of turns limit.")

        for attribute in args:
            print(
                "Attribute '{attribute}' hasn't been recognized! Ignoring."
                .format(
                    attribute=attribute,
                )
            )

        for key, value in kwargs.items():
            print(
                "Keyword '{key}' and it's value '{value}' hasn't been recognized! Ignoring."
                .format(
                    key=key,
                    value=value,
                )
            )

        self._turns_width = len(str(self._turns_limit))  # calculate width for `_turns_counter` formatting
        self._turns_counter = 1  # initialize turns counter
        self._solution = None  # initialize solution field
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution
        self._patterns_number = self._colors_number ** self._pegs_number  # calculate number of all possible patterns
        self._colors_list = list(range(self._colors_number))  # initialize list of colors

    @property
    def colors_number(self):
        """ Returns colors number """

        return self._colors_number

    @property
    def pegs_number(self):
        """ Returns pegs number """

        return self._pegs_number

    @property
    def turns_limit(self):
        """ Returns turns limit """

        return self._turns_limit

    @property
    def turns_counter(self):
        """ Returns turn counter """

        return self._turns_counter

    @property
    def solution(self):
        """ Returns formatted solution pattern only when game is ended """

        if self._game_status == 0:
            raise PermissionError("No access to the solution when game is active!")
        else:
            if self._solution is None:
                raise ValueError("No saved solution in this game!")
            else:
                return self._format_pattern(self._solution)

    @property
    def game_status(self):
        """ Returns game status """

        return self._game_status

    @property
    def patterns_number(self):
        """ Returns all possible patterns number """

        return self._patterns_number

    @property
    def colors_list(self):
        """ Returns formatted set of colors """

        return (
            "{{{set}}}"
            .format(
                set=", ".join(self._format_peg(peg) for peg in self._colors_list),
            )
        )

    @property
    def example_pattern(self):
        """ Returns formatted example pattern based on game settings """

        return self._format_pattern(self._get_random_pattern())

    def _get_random_pattern(self):
        """ Returns random pattern for generating the solution or giving a demo pattern """

        return tuple(
            randrange(0, self._colors_number)
            for _ in range(self._pegs_number)
        )

    def _format_turn_number(self, turn_number):
        """ Returns formatted `turn_number` """

        return (
            "{turn:>{width}d}"
            .format(
                turn=turn_number,
                width=self._turns_width,
            )
        )

    @staticmethod
    def _format_peg(peg):
        """ Returns formatted `peg` """

        return (
            "({peg})"
            .format(
                peg=chr(peg + 97),  # TODO: implement different styles of formatting pattern
            )
        )

    def _format_pattern(self, pattern):
        """ Returns formatted `pattern` """

        return (
            "[{pattern}]"
            .format(
                pattern="".join(self._format_peg(peg) for peg in pattern),
            )
        )

    def _format_response(self, response):
        """ Returns formatted `response` """

        blacks = response[0]
        whites = response[1]
        return (
            "●" * blacks
            + "○" * whites
            + "∙" * (self._pegs_number - blacks - whites)
            + " ({blacks}, {whites})".format(
                blacks=blacks,
                whites=whites,
            )
        )

    def _format_turn(self, turn_number, pattern, response):
        """ Returns formatted whole turn (`turn_number`, `pattern` and `response`) """

        return (
            "{turn}: {pattern} => {response}"
            .format(
                turn=self._format_turn_number(turn_number),
                pattern=self._format_pattern(pattern),
                response=self._format_response(response),
            )
        )

    @staticmethod
    def _decode_peg(peg_char):
        """ Returns `peg` converted from formatted `peg_char` """

        if len(peg_char) == 1:
            return ord(peg_char) - 97  # TODO: input digits, lowercase or uppercase letters
        else:
            return None

    def _decode_pattern(self, pattern_string):
        """ Returns `pattern` converted from formatted `pattern_string` """

        try:
            pattern = tuple(
                self._decode_peg(peg_char)
                for peg_char in pattern_string.strip().split(' ', maxsplit=self._pegs_number - 1)  # divide into pegs
            )
        except (TypeError, ValueError):
            return None

        if self._validate_pattern(pattern):
            return pattern
        else:
            return None

    def _decode_response(self, response_string):
        """ Returns `response` converted from formatted `response_string` """

        try:
            response = tuple(
                int(response_peg)
                for response_peg in response_string.strip().split(' ', maxsplit=1)  # only one divide
            )
        except (TypeError, ValueError):
            return None

        if self._validate_response(response):
            return response
        else:
            return None

    def _validate_pattern(self, pattern):
        """ Checks if given `pattern` is formally correct """

        return (
            isinstance(pattern, tuple)
            and len(pattern) == self._pegs_number
            and all(
                pattern_peg in self._colors_list
                for pattern_peg in pattern
            )
        )

    def _validate_response(self, response):
        """ Checks if given `response` (a tuple built from black pegs and white pegs) is formally correct """

        return (
            isinstance(response, tuple)
            and len(response) == 2
            and all(
                response_peg in range(0, self._pegs_number + 1)
                for response_peg in {response[0], response[1], response[0] + response[1]}
                # both black and white pegs number (and sum of them also) should be between 0 and pegs number
            )
        )

    def calculate_response(self, pattern1, pattern2):
        """ Returns calculated response (black and white pegs) for given pattern, related to other pattern """

        # `black_pegs` defines how many pegs are in proper color and in proper location
        black_pegs = sum(
            int(pattern1_peg == pattern2_peg)
            for pattern1_peg, pattern2_peg in zip(pattern1, pattern2)
        )

        # `black_white_pegs` defines how many pegs are in proper color regardless to location
        black_white_pegs = sum(
            min(pattern1.count(pattern_peg), pattern2.count(pattern_peg))
            for pattern_peg in self._colors_list
        )

        # `white_pegs` defines how many pegs are in proper color and wrong location
        # to calculate `white_pegs` it's needed to subtract `black_pegs` from `black_white_pegs`
        return black_pegs, black_white_pegs - black_pegs  # return response tuple with black and white pegs

    def _check_game_end(self, response):
        """ Checks if the game should end (after current turn) """

        if response == (self._pegs_number, 0):  # check if all response pegs are black  # TODO: response from class?
            self._game_status = 1  # solution is found
            return True

        if self._turns_counter >= self._turns_limit:
            self._game_status = 2  # reached turns limit
            return True

        return False


class MastermindGame(Mastermind):
    """ Contains Mastermind Game mode, inherits from Mastermind class """

    def __init__(self, *args, solution=None, **kwargs):
        """ Initializes Mastermind Game class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        if solution is None:  # check if `solution` is given
            self._solution = self._get_random_pattern()
        else:
            if self._validate_pattern(solution):
                self._solution = solution
            else:
                raise ValueError("Incorrect solution pattern.")

    @property
    def prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "Enter pattern number {turn}: "
            .format(
                turn=self._turns_counter,
            )
        )

    def take_turn_human(self, pattern_string):
        """ Gets `pattern_string` from human (CodeBreaker), verifies it, takes turn and returns formatted response """

        pattern = self._decode_pattern(pattern_string)
        if pattern is None:
            raise ValueError("Given pattern is incorrect! Enter again.")

        turn = self._turns_counter  # save counter before taking turn
        response = self.take_turn(pattern)
        print(self._format_turn(turn, pattern, response))  # TODO: print all turns

        return (  # TODO: print it instead returning it
            "{turn:>{width}d}: {pattern} -> {response}"
            .format(
                turn=turn,
                width=self._turns_width,
                pattern=self._format_pattern(pattern),
                response=self._format_response(response),
                )
            )

    def take_turn(self, pattern):
        """ Takes turn as CodeMaker (with pattern from CodeBreaker) - without pattern validation, returns response """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        response = self.calculate_response(pattern, self._solution)

        if not self._check_game_end(response):
            self._turns_counter += 1  # prepare for next turn

        return response


class MastermindSolver(Mastermind):
    """ Contains Mastermind Solver mode, inherits from Mastermind class """

    def __init__(self, *args, shuffle_mode=SHUFFLE_MODE, solve_mode=SOLVE_MODE, **kwargs):
        """ Initializes Mastermind Solver class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        # check if given `shuffle_mode` is correct
        if shuffle_mode in {0, 1, 2, 3}:
            self._shuffle_mode = shuffle_mode
        else:
            raise ValueError("Incorrect patterns shuffling mode.")

        # TODO: new flag needed: `self._first_turn`

        # check if given `solve_mode` is correct
        if solve_mode == 1:  # patterns checking generator mode
            self._solver = MastermindSolverMode1(self)  # TODO: giving (self) is OK?
        elif solve_mode == 2:  # patterns list filtering mode
            self._solver = MastermindSolverMode2(self)  # TODO: giving (self) is OK?
        else:
            raise ValueError("Incorrect solving mode.")

    @property
    def poss_number(self):
        """ Returns possible solutions number """

        return self._solver.poss_number

    @property
    def single_poss(self):
        """ Returns formatted single possible solution flag """

        return " This must be the solution, there is no other option!" if self._solver.single_poss else ""

    def get_patterns_list(self):
        """ Returns list of all pattern combinations using game settings """

        # generates all possible patterns using my own function
        # it's similar to Cartesian product (`import itertools.product`),
        # but operates on tuples (not lists) and works direct on Mastermind class variables

        # `_shuffle_mode`s are:
        # 0 = don't shuffle `_colors_list` during building; don't shuffle `all_patterns` after build
        # 1 =    do shuffle `_colors_list` during building; don't shuffle `all_patterns` after build
        # 2 = don't shuffle `_colors_list` during building;    do shuffle `all_patterns` after build
        # 3 =    do shuffle `_colors_list` during building;    do shuffle `all_patterns` after build

        all_patterns = [()]  # initialize with list containing empty tuple
        colors_list = self._colors_list  # get local `colors_list` to be shuffled (if needed)

        p = Progress("Building patterns list...", sum(self._colors_number**i for i in range(1, self._pegs_number + 1)))
        for _ in range(self._pegs_number):  # iterate for every peg

            if self._shuffle_mode in {1, 3}:  # shuffle `colors_list` to build patterns from (on every iteration)
                shuffle(colors_list)
            # else {0, 2}: don't shuffle `colors_list`, patterns will be in ascending order

            all_patterns = [
                p.item((*pattern, pattern_peg))  # (wrapped) new tuple one peg bigger (all "old" pegs + "new" one)
                for pattern in all_patterns  # all "old" pegs
                for pattern_peg in colors_list  # one "new" peg
            ]
        p.delete()

        if self._shuffle_mode in {2, 3}:  # shuffle `all_patterns` (at once)
            p = Progress("Shuffling patterns list...", len(all_patterns) - 1)
            shuffle(all_patterns, p_obj=p)
            p.delete()
        # else {0, 1}: don't shuffle `all_patterns`

        return all_patterns

    @property
    def prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "Turn number {turn}. Enter response for pattern {pattern}: "
            .format(
                turn=self._turns_counter,
                pattern=self._format_pattern(self._solver.current_poss),
            )
        )

    def take_turn_human(self, response_string):
        """ Gets `response_string` from human (CodeMaker), verifies it and takes turn """

        response = self._decode_response(response_string)
        if response is None:
            raise ValueError("Given response is incorrect! Enter again.")

        print(self._format_turn(self._turns_counter, self._solver.current_poss, response))  # TODO: print all turns

        pattern = self.take_turn(response)
        if pattern is None:  # TODO: delete this section? Return something else? Print it?
            return "No further possible solutions."
        else:
            return (
                "My next possible solution is {pattern}.{single}"
                .format(
                    pattern=self._format_pattern(pattern),  # TODO: current from Solver Mode
                    single=self.single_poss,
                )
            )
            print()

    def take_turn(self, response):
        """ Takes turn as CodeBreaker (with response from CodeMaker) - without response validation, returns pattern """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if self._check_game_end(response):
            if self._game_status == 1:  # if the solution is found
                self._solution = self._solver.current_poss  # save current possible solution as proper solution
            return None

        self._turns_counter += 1  # prepare for next turn # TODO: make it similar as in MastermindGame

        return self._solver.take_turn(response)

    # def _check_game_end(self, response):
    #     """ Checks if the game should end (after current turn) """
    #
    #     if super()._check_game_end(response):  # check if solution is found or reached turns limit
    #         return True
    #
    #     # TODO: active or passive checking?
    #     if self._solver.check_game_end():  # check if exists another possible solution
    #         print(self._game_status)
    #         self._game_status = 3  # no possible solution
    #         print(self._game_status)
    #         return True
    #
    #     return False


class MastermindSolverMode1:
    """ Contains Mastermind Solver MODE 1 (patterns checking generator mode) """

    def __init__(self, upper):
        """ (MODE 1) Initializes Mastermind Solver MODE 1 class object """

        self.super = upper  # TODO: is it OK?

        self._turns = dict()  # initialize dictionary of turns
        self._poss_state = self._poss_generator()  # initialize possible solutions generator
        self._single_poss = False  # initialize the single possible solution flag
        self._second_poss = None  # TODO: temporary
        self._current_poss = self._get_next_poss()  # get first possible solution

    @property
    def current_poss(self):
        """ (MODE 1) Returns current possible solution (in this turn) """

        return self._current_poss

    @property
    def single_poss(self):
        """ (MODE 1) Returns single possible solution flag """

        return self._single_poss

    @property
    def poss_number(self):
        """ (MODE 1) Returns possible solutions number """

        raise NotImplementedError("It is impossible to calculate possible solutions number in (MODE 1)!")

    def take_turn(self, response):
        """ (MODE 1) Takes turn as CodeBreaker with response and returns next possible solution """

        self._turns[self._current_poss] = response  # add this turn to the turns dictionary

        self._current_poss = self._get_next_poss()  # get next possible solution
        return self._current_poss

    def _poss_generator(self):
        """ (MODE 1) Yields the first possible solution based on all previous turns """

        poss_counter = 0  # initialize possible solutions counter
        poss_list = self.super.get_patterns_list()  # get list of all possible solutions to be checked
        poss_number = self.super.patterns_number  # get number of all patterns

        p = Progress("Thinking...", poss_number)
        for poss in poss_list:  # TODO: progress
            poss_counter += 1
            p.item()  # TODO: repair it

            if self._check_poss(poss):
                print(
                    "(MODE 1) Found possible solution.",
                    "It's index is {index} of {all} overall ({percent:.2f}%)."
                    .format(
                        index=poss_counter,
                        all=poss_number,
                        percent=100 * poss_counter / poss_number,
                    )
                )
                yield poss  # yields pattern if it can be a solution

        # after yield the last pattern
        p.delete()  # TODO: repair it
        print(
            "(MODE 1) Finished searching for possible solutions.",
            "Reached index {index} of {all} overall ({percent:.2f}%)."  # should be always 100.00%
            .format(
                index=poss_counter,
                all=poss_number,
                percent=100 * poss_counter / poss_number,
            )
        )

    def _check_poss(self, poss):
        """ (MODE 1) Checks if given possible solution still can be a solution based on all previous turns """

        return all(
            self.super.calculate_response(turn_pattern, poss) == turn_response
            for turn_pattern, turn_response in self._turns.items()
        )

    def _get_next_poss(self):
        """ (MODE 1) Returns next possible solution (if exists) """

        self._single_poss = False  # reset the flag

        # check if previously found possible solution still can be a solution
        if self._second_poss is not None and self._check_poss(self._second_poss):
            # TODO: change `if` criteria (especially when `_second_poss` will be disabled)
            print("(MODE 1) Previously found second possible solution still can be a solution.")
            current_poss = self._second_poss  # yes -> save it as current possible solution
        else:
            print("(MODE 1) Searching for possible solution...")  # TODO: progress?
            try:
                current_poss = next(self._poss_state)  # no -> get another possible solution
            except StopIteration:
                self.super._game_status = 3  # no solution found  # TODO: setter?
                self._second_poss = None  # there is also no second possible solution
                return None

        print("(MODE 1) Searching for second possible solution...")  # TODO: progress?
        try:
            self._second_poss = next(self._poss_state)  # get second possible solution
        except StopIteration:  # there is no second solution -> only one solution!
            self._single_poss = True  # set the flag
            self._second_poss = None

        return current_poss

    # def check_game_end(self):
    #     """ (MODE 1) Checks if the game should end (after current turn) """
    #
    #     if self._second_poss is None:  # TODO: for tests - delete this method?
    #         print("(MODE 1) END!")
    #
    #     return self._second_poss is None  # `True` if there were only one possible solution
    #     # TODO: change it when `_second_poss` will be disabled - always return False?


class MastermindSolverMode2:
    """ Contains Mastermind Solver MODE 2 (patterns list filtering mode) """

    def __init__(self, upper):
        """ (MODE 2) Initializes Mastermind Solver MODE 2 class object """

        self.super = upper  # TODO: is it OK?

        self._poss_list = self.super.get_patterns_list()  # get list of all possible solutions to be filtered
        self._single_poss = False  # initialize the single possible solution flag
        self._current_poss = self._get_next_poss()  # get first possible solution

    @property
    def current_poss(self):
        """ (MODE 2) Returns current possible solution (in this turn) """

        return self._current_poss

    @property
    def single_poss(self):
        """ (MODE 2) Returns single possible solution flag """

        return self._single_poss

    @property
    def poss_number(self):
        """ (MODE 2) Returns possible solutions number """

        return len(self._poss_list)

    def take_turn(self, response):
        """ (MODE 2) Takes turn as CodeBreaker with response and returns next possible solution """

        old_number = self.poss_number

        p = Progress("(MODE 2) Filtering patterns list...", old_number)
        # TODO: maybe remove items from list that don't meet condition?
        self._poss_list = [  # filter the existing list
            pattern
            for pattern in self._poss_list
            if p.item(self.super.calculate_response(self._current_poss, pattern) == response)  # wrapped with p.item()
        ]
        p.delete()

        new_number = self.poss_number
        print(
            "(MODE 2) Number of possible solutions is now {new} of {old} (rejected {percent:.2f}% of patterns)."
            .format(
                new=new_number,
                old=old_number,
                percent=100 * (1 - new_number / old_number),
            )
        )

        self._current_poss = self._get_next_poss()  # get next possible solution
        return self._current_poss

    def _get_next_poss(self):
        """ (MODE 2) Returns next possible solution (if exists) """

        number = self.poss_number  # get the possible solutions number
        self._single_poss = (number == 1)  # set the flag if there is only one possible solution

        if number:  # check if there is at least one possible solution
            return self._poss_list[0]  # take first possible solution from the list
            # TODO: maybe random value? Not always 0? - parameter
        else:
            self.super._game_status = 3  # no solution found  # TODO: setter?
            return None

    def check_game_end(self):
        """ (MODE 2) Checks if the game should end (after current turn) """

    # def check_game_end(self):
    #     """ (MODE 2) Checks if the game should end (after current turn) """
    #
    #     if self.poss_number <= 1:  # TODO: for tests - delete this method?
    #         print("(MODE 2) END!")
    #
    #     return self.poss_number <= 1  # `True` if there were only one possible solution (or less)
