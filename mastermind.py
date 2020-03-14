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
        self._turns = []  # initialize list of turns
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
    def turns(self):
        """ Returns turns list """

        return self._turns

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

    def _format_turn_count(self, turn_count):
        """ Returns formatted `turn_count` """

        return (
            "{turn_count:>{width}d}"
            .format(
                turn_count=turn_count,
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

        black_number = response[0]
        white_number = response[1]
        return (
            "[{blacks}{whites}{dots}] ({black_number}, {white_number})"
            .format(
                blacks="●" * black_number,
                whites="○" * white_number,
                dots="∙" * (self._pegs_number - black_number - white_number),
                black_number=black_number,
                white_number=white_number,
            )
        )

    def _format_turn(self, turn_count, pattern, response):
        """ Returns formatted whole turn (`turn_count`, `pattern` and `response`) """

        return (
            "{turn_count}. {pattern} => {response}"
            .format(
                turn_count=self._format_turn_count(turn_count),
                pattern=self._format_pattern(pattern),
                response=self._format_response(response),
            )
        )

    def print_turns(self):
        """ Prints all turns """

        print()
        for turn_number, (pattern, response) in enumerate(self._turns, 1):
            print(self._format_turn(turn_number, pattern, response))

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

        self._turns_counter += 1  # prepare for next turn
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
    def game_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{turn_count}. Enter pattern: "
            .format(
                turn_count=self._format_turn_count(self._turns_counter),
            )
        )

    def game_take_turn(self, pattern_string, pattern=None):
        """ Takes turn as CodeMaker (with `pattern` or `pattern_string` from CodeBreaker) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if pattern is None:
            pattern = self._decode_pattern(pattern_string)
            if pattern is None:
                raise ValueError("Given pattern is incorrect! Enter again.")

        response = self.calculate_response(pattern, self._solution)  # TODO: save response to class object?
        self._turns.append((pattern, response))  # add turn (as a tuple) to the `turns` list

        self.print_turns()

        self._check_game_end(response)


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
            self._solve_mode = 1
            self._solver = MastermindSolverMode1(self)  # TODO: giving (self) is OK?
        elif solve_mode == 2:  # patterns list filtering mode
            self._solve_mode = 2
            self._solver = MastermindSolverMode2(self)  # TODO: giving (self) is OK?
        else:
            raise ValueError("Incorrect solving mode.")

    @property
    def shuffle_mode(self):
        """ Returns shuffle mode number """

        return self._shuffle_mode

    @property
    def solve_mode(self):
        """ Returns solve mode number """

        return self._solve_mode

    @property
    def poss_number(self):
        """ Returns possible solutions number """

        return self._solver.poss_number

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

        operations_number = sum(self._colors_number ** i for i in range(1, self._pegs_number + 1))
        progress = Progress("Building patterns list...", operations_number)
        progress.start()
        for _ in range(self._pegs_number):  # iterate for every peg

            if self._shuffle_mode in {1, 3}:  # shuffle `colors_list` to build patterns from (on every iteration)
                shuffle(colors_list)
            # else {0, 2}: don't shuffle `colors_list`, patterns will be in ascending order

            all_patterns = [
                (*pattern, progress.item(pattern_peg))  # new tuple one peg bigger ("old" pegs + "new" (wrapped) one)
                for pattern in all_patterns  # all "old" pegs
                for pattern_peg in colors_list  # one "new" peg
            ]
        progress.stop()

        if self._shuffle_mode in {2, 3}:  # shuffle `all_patterns` (at once)
            progress = Progress("Shuffling patterns list...", len(all_patterns) - 1)
            progress.start()
            shuffle(all_patterns, progress=progress)  # TODO: one line, without `progress` variable
            progress.stop()
        # else {0, 1}: don't shuffle `all_patterns`

        return all_patterns

    @property
    def solver_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{turn_count}. Enter response for pattern {pattern}: "
            .format(
                turn_count=self._format_turn_count(self._turns_counter),
                pattern=self._format_pattern(self._solver.current_poss),
            )
        )

    def solver_take_turn(self, response_string, response=None):
        """ Takes turn as CodeBreaker (with `response` or `response_string` from CodeMaker) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if response is None:
            response = self._decode_response(response_string)
            if response is None:
                raise ValueError("Given response is incorrect! Enter again.")

        current_poss = self._solver.current_poss
        self._turns.append((current_poss, response))  # add turn (as a tuple) to the `turns` list

        self.print_turns()

        if self._check_game_end(response):
            if self._game_status == 1:  # if the solution is found
                self._solution = current_poss  # save current possible solution as proper solution
        else:
            next_poss = self._solver.calculate_poss(current_poss, response)
            if next_poss is None:
                self._game_status = 3  # no possible solution found

            if self._solver.single_poss and self.game_status == 0:
                print("Now I know there is only one possible solution!")


class MastermindSolverMode1:
    """ Contains Mastermind Solver MODE 1 (patterns checking generator mode) """

    def __init__(self, upper):
        """ (MODE 1) Initializes Mastermind Solver MODE 1 class object """

        self.super = upper  # TODO: is it OK?

        self._generator = MastermindSolverMode1Generator(self)  # initialize possible solutions generator
        self._current_poss = None  # initialize current possible solution
        self._second_poss = None  # initialize second possible solution
        self._single_poss = False  # initialize single possible solution flag

        self._get_next_poss()  # get first possible solution

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

        raise NotImplementedError("It is impossible to calculate possible solutions number in MODE 1!")

    def check_poss(self, poss):
        """ (MODE 1) Checks if given possible solution still can be a solution based on all previous turns """

        return all(
            self.super.calculate_response(turn_pattern, poss) == turn_response
            for turn_pattern, turn_response in self.super.turns
        )

    def calculate_poss(self, turn_pattern, turn_response):
        """ (MODE 1) Calculates the next possible solution after current turn """

        self._get_next_poss()  # get next possible solution
        return self._current_poss

    def _get_next_poss(self):
        """ (MODE 1) Saves next possible solution (if exists) """

        self._single_poss = False  # reset the flag

        # TODO: change `if` criteria (especially when `_second_poss` will be disabled)

        if self._current_poss is not None and self.check_poss(self._current_poss):
            print("Previously found first possible solution still can be a first solution. Not changed.")
        else:
            if self._second_poss is not None and self.check_poss(self._second_poss):
                print("Previously found second possible solution still can be a solution. Saved as first.")
                self._current_poss = self._second_poss
                self._second_poss = None
            else:
                try:
                    self._current_poss = self._generator.next("Searching for first possible solution...")
                except StopIteration:
                    self._current_poss = None  # no possible solution
                    self._second_poss = None  # no second possible solution also
                    return

        if self._second_poss is not None and self.check_poss(self._second_poss):
            print("Previously found second possible solution still can be a second solution. Not changed.")
        else:
            try:
                self._second_poss = self._generator.next("Searching for second possible solution...")
            except StopIteration:  # there is no second solution -> only one solution!
                self._single_poss = True  # set the flag
                self._second_poss = None  # no second possible solution


class MastermindSolverMode1Generator:
    """ (MODE 1) Contains possible solutions generator """

    def __init__(self, upper):
        """ (MODE 1 Generator) Initializes Mastermind Solver MODE 1 Generator class object """

        self.super = upper

        self._list = self.super.super.get_patterns_list()  # get list of all possible solutions to be checked
        self._index = 0  # initialize possible solutions index
        self._all = len(self._list)

        self._progress = Progress("", self._all)  # initializes Progress class object to display generation progress

    def next(self, text=None):
        """ (MODE 1 Generator) Returns the first possible solution based on all previous turns """

        if text is not None:
            self._progress.rename(text)  # change the displayed text when needed

        while self._index < self._all:  # index between 0 and len()-1
            poss = self._list[self._index]  # get pattern from list
            self._index += 1  # now index is between 1 and len()

            if self._progress.item(self.super.check_poss(poss)):  # wrapped the long-taking operation
                self._progress.stop(
                    "Found! It's index is {index} of {all} overall ({percent:.2f}%)."
                    .format(
                        index=self._index,
                        all=self._all,
                        percent=100 * self._index / self._all,
                    )
                )
                return poss

        # after return the last pattern
        self._progress.stop(
            "Finished. Reached index {index} of {all} overall ({percent:.2f}%)."
            .format(
                index=self._index,
                all=self._all,
                percent=100 * self._index / self._all,  # should be always 100.00%
            )
        )
        raise StopIteration


class MastermindSolverMode2:
    """ Contains Mastermind Solver MODE 2 (patterns list filtering mode) """

    def __init__(self, upper):
        """ (MODE 2) Initializes Mastermind Solver MODE 2 class object """

        self.super = upper  # TODO: is it OK?

        self._poss_list = self.super.get_patterns_list()  # get list of all possible solutions to be filtered
        self._current_poss = None  # initialize current possible solution
        self._single_poss = False  # initialize single possible solution flag

        self._get_next_poss()  # get first possible solution

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

    def calculate_poss(self, turn_pattern, turn_response):
        """ (MODE 2) Calculates the next possible solution after current turn """

        old_number = self.poss_number

        progress = Progress("Filtering patterns list...", old_number)
        progress.start()
        # TODO: maybe remove items from list that don't meet condition?
        self._poss_list = [  # filter the existing list
            poss_pattern
            for poss_pattern in self._poss_list
            if progress.item(self.super.calculate_response(turn_pattern, poss_pattern) == turn_response)  # wrapped
        ]
        progress.stop()

        new_number = self.poss_number
        print(
            "Number of possible solutions is now {new} of {old} (rejected {percent:.2f}% of patterns)."
            .format(
                new=new_number,
                old=old_number,
                percent=100 * (1 - new_number / old_number),
            )
        )

        self._get_next_poss()  # get next possible solution
        return self._current_poss

    def _get_next_poss(self):
        """ (MODE 2) Saves next possible solution (if exists) """

        number = self.poss_number  # get the possible solutions number
        self._single_poss = (number == 1)  # set the flag if there is only one possible solution

        if number:  # check if there is at least one possible solution
            self._current_poss = self._poss_list[0]  # take first possible solution from the list
            # TODO: maybe random value? Not always 0? - parameter
        else:
            self._current_poss = None
