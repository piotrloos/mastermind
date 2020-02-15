########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main class file                      #
#             Piotr Loos (c) 2019-2020 #
########################################

from abc import abstractmethod
from random import randint, sample
from settings import *


class Mastermind:
    """ Contains whole game, base class for CodeMaker and CodeBreaker classes """

    @abstractmethod
    def __init__(self, colors=COLORS, pegs=PEGS, turns_limit=TURNS_LIMIT, gen_mode=GEN_MODE, shuffle_mode=SHUFFLE_MODE):
        """ Initializes new game with given settings """

        # check if given `colors` number is correct
        if colors in range(2, 11):  # from 2 to 10
            self._colors_number = colors
        else:
            raise ValueError("Incorrect number of colors.")

        # check if given `pegs` number is correct
        if pegs in range(2, 9):  # from 2 to 8
            self._pegs_number = pegs
        else:
            raise ValueError("Incorrect number of pegs.")

        # check if given `turns_limit` number is correct
        if turns_limit in range(1, 21):  # from 1 to 20
            self._turns_limit = turns_limit
        else:
            raise ValueError("Incorrect number of turns limit.")

        # check if given patterns `gen_mode` is correct
        if gen_mode in {1, 2}:  # 1 or 2
            self._gen_mode = gen_mode
        else:
            raise ValueError("Incorrect patterns generation mode.")

        # check if given patterns `shuffle_mode` is correct
        if shuffle_mode in {0, 1, 2, 3}:
            self._shuffle_mode = shuffle_mode
        else:
            raise ValueError("Incorrect patterns shuffle mode.")

        self._turns_width = len(str(self._turns_limit))  # calculate width for `_turns_counter` formatting
        self._turns_counter = 1  # initialize turns counter
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution
        self._patterns_number = self._colors_number ** self._pegs_number  # calculate number of all possible patterns
        self._solution_pattern = None  # initialize object variable for solution pattern
        self._colors_set = set(range(self._colors_number))  # initialize set of colors (for performance)

    @property
    def colors_number(self):
        return self._colors_number

    @property
    def pegs_number(self):
        return self._pegs_number

    @property
    def turns_limit(self):
        return self._turns_limit

    @property
    def turns_counter(self):
        return self._turns_counter

    @property
    def game_status(self):
        return self._game_status

    @property
    def patterns_number(self):
        return self._patterns_number

    @property
    def solution_pattern(self):
        """ Returns formatted solution pattern only when game is ended """

        if self._game_status == 0:
            raise PermissionError("No access to the solution when game is active.")
        else:
            return self._format_pattern(self._solution_pattern)

    @property
    def colors_set(self):
        """ Returns formatted set of colors """

        return "{" + ", ".join(self._encode_peg(peg_int) for peg_int in self._colors_set) + "}"

    @property
    def example_pattern(self):
        """ Returns formatted example pattern based on game settings """

        return self._format_pattern(self._get_random_pattern())

    def _get_random_pattern(self):
        """ Returns random pattern for generating solution or giving a demo pattern """

        return tuple(randint(0, self._colors_number - 1) for _ in range(self._pegs_number))

    def _format_pattern(self, pattern):
        """ Returns formatted pattern """

        return "[ " + " ".join(self._encode_peg(peg_int) for peg_int in pattern) + " ]"

    @staticmethod
    def _encode_peg(peg_int):
        """ Returns formatted peg (char) converted from integer """

        return chr(peg_int + 97)  # TODO: implement different styles of formatting pattern

    @staticmethod
    def _decode_peg(peg_char):
        """ Returns integer converted from formatted peg (char) """

        if len(peg_char) == 1:
            return ord(peg_char) - 97  # TODO: input digits, lowercase or uppercase letters
        else:
            return None

    def _get_patterns_list(self):
        """ Returns list of all pattern combinations using game settings """

        # generates all possible patterns using my own function
        # it's similar to Cartesian product (`import itertools.product`),
        # but operates on tuples (not lists) and works direct on Mastermind class variables

        all_patterns = (),  # initialize `all_patterns` with tuple containing empty tuple

        # `_shuffle_mode`s are:
        # 0 = don't shuffle `_colors_set` before build; don't shuffle `all_patterns` after build
        # 1 =    do shuffle `_colors_set` before build; don't shuffle `all_patterns` after build
        # 2 = don't shuffle `_colors_set` before build;    do shuffle `all_patterns` after build
        # 3 =    do shuffle `_colors_set` before build;    do shuffle `all_patterns` after build

        # build list (in fact generator for last peg) of all possible patterns
        if self._shuffle_mode in {1, 3}:  # shuffle `_colors_set` to build patterns from (on every iteration)
            for _ in range(self._pegs_number):
                all_patterns = (
                    (*pattern, pattern_peg)
                    for pattern in all_patterns
                    for pattern_peg in sample(self._colors_set, self._colors_number)  # `sample` returns a new list
                )
        else:  # {0, 2} - don't shuffle `_colors_set`, so `all_patterns` will contain patterns in ascending order
            for _ in range(self._pegs_number):
                all_patterns = (
                    (*pattern, pattern_peg)
                    for pattern in all_patterns
                    for pattern_peg in self._colors_set
                )

        if self._shuffle_mode in {2, 3}:  # shuffle `all_patterns` (at once)
            all_patterns = sample(set(all_patterns), self._patterns_number)  # `all_patterns` are now list, not gen.
        # else {0, 1} - don't shuffle `all_patterns` -> nothing to do

        return all_patterns

    def _calculate_response(self, pattern1, pattern2=None):
        """ Returns calculated response (black and white pegs) for given pattern """

        # there is a possibility to calculate response for pattern relative to another pattern, not always the solution
        if pattern2 is None:
            if self._solution_pattern is None:
                raise ValueError("No solution pattern to calculate response.")
            else:
                pattern2 = self._solution_pattern

        # `black_pegs` defines how many pegs are in proper color and in proper location
        black_pegs = sum(
            int(pattern1_peg == pattern2_peg)
            for pattern1_peg, pattern2_peg in zip(pattern1, pattern2)
        )

        # `black_white_pegs` defines how many pegs are in proper color regardless to location
        black_white_pegs = sum(
            min(pattern1.count(pattern_peg), pattern2.count(pattern_peg))
            for pattern_peg in self._colors_set
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


class CodeMaker(Mastermind):
    """ Contains CodeMaker mode, inherits from Mastermind class """

    def __init__(self, solution=None, **kwargs):
        """ Initializes CodeMaker class object """

        super().__init__(**kwargs)  # initialize Mastermind class object

        # check if `solution` is given, if not -> randomize new pattern
        if solution is None:
            self._solution_pattern = self._get_random_pattern()
        else:
            # check if given `solution` is correct
            if self._validate_pattern(solution):
                self._solution_pattern = solution
            else:
                raise ValueError("Incorrect solution pattern.")

    @property
    def prompt(self):
        """ Returns prompt string for input function """

        return (
            "Enter pattern number {turn}: "
            .format(
                turn=self._turns_counter,
            )
        )

    def _validate_pattern(self, pattern):
        """ Checks if given `pattern` is formally correct """

        return (
            isinstance(pattern, tuple)
            and len(pattern) == self._pegs_number
            and all(pattern_peg in self._colors_set for pattern_peg in pattern)
        )

    def input_for_codemaker(self, pattern_string):
        """ Takes `pattern_string` from CodeBreaker (human), verifies it, takes turn and returns formatted response """

        try:  # try to convert `pattern_string` to tuple (pattern format)
            pattern = tuple(
                self._decode_peg(peg_char)
                for peg_char in pattern_string.strip().split(' ', maxsplit=self._pegs_number - 1)  # divide into pegs
            )
        except (TypeError, ValueError):
            raise ValueError("Given pattern is incorrect! Enter again.")

        if not self._validate_pattern(pattern):  # check if `pattern` is correct
            raise ValueError("Given pattern is incorrect! Enter again.")

        return (
            "{turn:>{width}d}: {pattern} -> {response}"
            .format(
                turn=self._turns_counter,
                width=self._turns_width,
                pattern=self._format_pattern(pattern),
                response=self.take_turn_as_codemaker(pattern),
                )
            )

    def take_turn_as_codemaker(self, pattern):
        """ Takes turn as CodeMaker (with pattern from CodeBreaker) - without pattern validation, returns response """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        response = self._calculate_response(pattern)

        if not self._check_game_end(response):
            self._turns_counter += 1  # prepare for next turn

        return response


class CodeBreaker(Mastermind):
    """ Contains CodeBreaker mode, inherits from Mastermind class """

    def __init__(self, **kwargs):  # TODO: add new param - next_hint mode or calc solutions_number mode
        """ Initializes CodeBreaker class object """

        super().__init__(**kwargs)  # initialize Mastermind class object

        self._single_solution = False  # initialize the `_single_solution` flag

        if self._gen_mode == 1:  # checking patterns generator mode
            self._1turns = dict()  # initialize dictionary of turns
            self._1hint = self._1hint_generator()  # initialize hint pattern generator
            self._current_pattern = self._1hint_next()  # get first pattern
            self._1second_pattern = self._1hint_next(set_status=False)  # get second pattern
        elif self._gen_mode == 2:  # patterns list filtering mode
            self._2patterns = list(self._get_patterns_list())  # prepare list of all possible patterns to filter
            self._current_pattern = self._2patterns[0]  # take first pattern from the list

    @property
    def current_pattern(self):
        """ Returns formatted `current_pattern` string """

        return self._format_pattern(self._current_pattern)

    @property
    def hint_percent(self):
        """ Returns current hint percentage value """

        return 100 * self._1hint_counter / self._patterns_number

    @property
    def single_solution(self):
        """ Returns formatted `_single_solution` string (asterisk) """

        return " (*)" if self._single_solution else ""

    @property
    def prompt(self):
        """ Returns prompt string for input function """

        return (
            "Turn number {turn}. Enter response for pattern {pattern}{single}: "
            .format(
                turn=self._turns_counter,
                pattern=self.current_pattern,  # formatted
                single=self.single_solution,  # formatted
            )
        )

    def _validate_response(self, response):
        """ Checks if given response (a tuple built from black pegs and white pegs) is formally correct """

        return (
            isinstance(response, tuple)
            and len(response) == 2
            and all(
                response_peg in range(0, self._pegs_number + 1)
                for response_peg in {response[0], response[1], response[0] + response[1]}
                # both black and white pegs number (and sum of them also) should be between 0 and pegs number
            )
        )

    def input_for_codebreaker(self, response_string):
        """ Takes `response_string` from CodeMaker (human), verifies it, takes turn and returns formatted pattern """

        try:  # try to convert `response_string` to tuple (response format)
            response = tuple(
                int(response_peg) for response_peg in response_string.strip().split(' ', maxsplit=1)  # only one divide
            )
        except (TypeError, ValueError):
            raise ValueError("Given response is incorrect! Enter again.")

        if not self._validate_response(response):  # check if `response` is correct
            raise ValueError("Given response is incorrect! Enter again.")

        pattern = self.take_turn_as_codebreaker(response)

        if pattern is None:
            return "No further pattern to guess."
        else:
            return (
                "My next pattern is {pattern}{single}."
                .format(
                    pattern=self._format_pattern(pattern),  # formatted
                    single=self.single_solution,  # formatted
                )
            )

    def take_turn_as_codebreaker(self, response):
        """ Takes turn as CodeBreaker (with response from CodeMaker) - without response validation, returns pattern """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if self._check_game_end(response):
            return None

        self._turns_counter += 1  # prepare for next turn

        if self._gen_mode == 1:  # checking patterns generator mode

            self._1turns[self._current_pattern] = response  # add this turn to the turns dictionary

            # check if previously generated pattern (`_1second_pattern`) still can be a solution
            if self._1hint_check(self._1second_pattern):
                self._current_pattern = self._1second_pattern  # yes -> save `_1second_pattern` as current
            else:
                self._current_pattern = self._1hint_next()  # no -> get another pattern

            self._1second_pattern = self._1hint_next(set_status=False)  # get second possible solution (if exists)
            self._single_solution = self._current_pattern is not None and self._1second_pattern is None  # set flag

        elif self._gen_mode == 2:  # patterns list filtering mode

            print("(2) before filter: {}".format(len(self._2patterns)))  # TODO: for tests

            self._2patterns = [  # filter the list
                pattern
                for pattern in self._2patterns
                if self._calculate_response(self._current_pattern, pattern) == response
            ]
            self._current_pattern = self._2patterns[0]  # take first pattern from the list
            self._single_solution = (len(self._2patterns) == 1)  # set flag

            print("(2) after filter: {}".format(len(self._2patterns)))  # TODO: for tests

        return self._current_pattern

    def _check_game_end(self, response):
        """ Checks if the game should end (after current turn) """

        if super()._check_game_end(response):
            return True

        if (
            self._gen_mode == 1 and self._1second_pattern is None  # check if exists another solution in `_gen_mode` = 1
        ) or (
            self._gen_mode == 2 and len(self._2patterns) <= 1  # check if exists another solution in `_gen_mode` = 2
        ):
            self._game_status = 3  # no possible solution
            return True

        return False

    def _1hint_generator(self):
        """ Yields the first pattern that can be a solution based on all previous turns """

        self._1hint_counter = 0  # initialize hint counter
        width = len(str(self._patterns_number))  # tests  # TODO: move out from there

        for hint_pattern in self._get_patterns_list():
            self._1hint_counter += 1

            if self._1hint_check(hint_pattern):
                print(  # tests  # TODO: move out from there
                    "(1) {hint:>{width}d} / {all:>{width}d} ({percent:6.2f}%)"
                    .format(
                        hint=self._1hint_counter,
                        all=self.patterns_number,
                        percent=self.hint_percent,
                        width=width,
                    )
                )
                yield hint_pattern  # yields pattern if it can be a solution

        # after yield the last pattern
        print(  # tests  # TODO: move out from there
            "(1) {hint:>{width}d} / {all:>{width}d} ({percent:6.2f}%)"  # should be always 100.00%
            .format(
                hint=self._1hint_counter,
                all=self.patterns_number,
                percent=self.hint_percent,
                width=width,
            )
        )

    def _1hint_check(self, hint_pattern):
        """ Checks if given `hint_pattern` can be a solution based on all previous turns """

        return all(
            self._1turns[turn_pattern] == self._calculate_response(turn_pattern, hint_pattern)
            for turn_pattern in self._1turns.keys()
        )

    def _1hint_next(self, set_status=True):
        """ Gets the next hint pattern and handles the `StopIteration` exception """

        try:
            return next(self._1hint)
        except StopIteration:
            if set_status:
                self._game_status = 3
            return None
