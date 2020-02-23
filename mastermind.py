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
    def __init__(self, colors=COLORS, pegs=PEGS, turns_limit=TURNS_LIMIT):  # TODO: kwargs to be ignored
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

        self._turns_width = len(str(self._turns_limit))  # calculate width for `_turns_counter` formatting
        self._turns_counter = 1  # initialize turns counter
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution
        self._patterns_number = self._colors_number ** self._pegs_number  # calculate number of all possible patterns
        self._colors_list = list(range(self._colors_number))  # initialize list of colors (for performance)

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
    def colors_list(self):
        return self._colors_list

    @property
    def colors_set(self):
        """ Returns formatted set of colors """

        return "{" + ", ".join(self._encode_peg(peg_int) for peg_int in self._colors_list) + "}"

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

    def __init__(self, solution=None, **kwargs):
        """ Initializes Mastermind Game class object """

        super().__init__(**kwargs)  # initialize Mastermind class object

        if solution is None:  # check if `solution` is given, if not -> randomize new pattern
            self._solution = self._get_random_pattern()
        else:
            if self._validate_pattern(solution):  # check if given `solution` is correct
                self._solution = solution
            else:
                raise ValueError("Incorrect solution pattern.")

    @property
    def solution(self):
        """ Returns formatted solution pattern only when game is ended """

        if self._game_status == 0:
            raise PermissionError("No access to the solution when game is active!")
        else:
            return self._format_pattern(self._solution)

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
            and all(
                pattern_peg in self._colors_list
                for pattern_peg in pattern
            )
        )

    def _calculate_response(self, pattern):
        """ Returns calculated response (black and white pegs) for given pattern, related to the solution """

        return super().calculate_response(pattern, self._solution)

    def input(self, pattern_string):
        """ Gets `pattern_string` from human (CodeBreaker), verifies it, takes turn and returns formatted response """

        try:  # try to convert `pattern_string` to tuple (pattern format)
            pattern = tuple(
                self._decode_peg(peg_char)
                for peg_char in pattern_string.strip().split(' ', maxsplit=self._pegs_number - 1)  # divide into pegs
            )
        except (TypeError, ValueError):
            raise ValueError("Given pattern is incorrect! Enter again.")

        if not self._validate_pattern(pattern):  # check if `pattern` is correct
            raise ValueError("Given pattern is incorrect! Enter again.")

        turn = self._turns_counter  # save counter before taking turn
        response = self.take_turn(pattern)

        return (
            "{turn:>{width}d}: {pattern} -> {response}"
            .format(
                turn=turn,
                width=self._turns_width,
                pattern=self._format_pattern(pattern),
                response=response,
                )
            )

    def take_turn(self, pattern):
        """ Takes turn as CodeMaker (with pattern from CodeBreaker) - without pattern validation, returns response """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        response = self._calculate_response(pattern)

        if not self._check_game_end(response):
            self._turns_counter += 1  # prepare for next turn

        return response


class MastermindSolver(Mastermind):
    """ Contains Mastermind Solver mode, inherits from Mastermind class """

    def __init__(self, shuffle_mode=SHUFFLE_MODE, solve_mode=SOLVE_MODE, **kwargs):
        """ Initializes Mastermind Solver class object """

        super().__init__(**kwargs)  # initialize Mastermind class object

        # check if given `shuffle_mode` is correct
        if shuffle_mode in {0, 1, 2, 3}:
            self._shuffle_mode = shuffle_mode
        else:
            raise ValueError("Incorrect patterns shuffling mode.")

        self._single_poss_sol = False  # initialize the single possible solution flag

        # TODO: new flag needed: `self._first_turn`

        # check if given `solve_mode` is correct
        if solve_mode == 1:  # patterns checking generator mode
            self._solver = MastermindSolverMode1(self)  # TODO: giving (self) is OK?
        elif solve_mode == 2:  # patterns list filtering mode
            self._solver = MastermindSolverMode2(self)  # TODO: giving (self) is OK?
        else:
            raise ValueError("Incorrect solving mode.")

    @property
    def shuffle_mode(self):
        return self._shuffle_mode

    @property
    def current_poss_sol(self):
        """ ... """

        return self._solver.mode_current_poss_sol

    @property
    def format_current_poss_sol(self):
        """ Returns formatted current possible solution string """

        return self._format_pattern(self.current_poss_sol)

    @property
    def poss_sol_number(self):
        """ Returns possible solutions number in solving mode 2, raises exception in solving mode 1 """

        return self._solver.mode_poss_sol_number

    @property
    def format_single_poss_sol(self):
        """ Returns formatted single possible solution flag as a string """

        return " This must be the solution, there is no other option!" if self._single_poss_sol else ""
        # TODO: get variable from modes

    @property
    def prompt(self):
        """ Returns prompt string for input function """

        return (
            "Turn number {turn}. Enter response for pattern {pattern}: "
            .format(
                turn=self._turns_counter,
                pattern=self.format_current_poss_sol,
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
        colors_list = self.colors_list

        # TODO: progress tests
        p = Progress("Building patterns list...", sum(self._colors_number**i for i in range(1, self._pegs_number + 1)))
        for _ in range(self._pegs_number):  # build list of all possible patterns

            if self._shuffle_mode in {1, 3}:  # shuffle `colors_list` to build patterns from (on every iteration)
                shuffle(colors_list)
            # else {0, 2}: don't shuffle `colors_list`, patterns will be in ascending order

            all_patterns = [
                p.item((*pattern, pattern_peg))  # new tuple one peg bigger (all "old" pegs + "new" one)
                for pattern in all_patterns  # all "old" pegs
                for pattern_peg in colors_list  # one "new" peg
            ]
        p.delete()

        # TODO: progress tests
        if self._shuffle_mode in {2, 3}:  # shuffle `all_patterns` (at once)
            p = Progress("Shuffling patterns list...", len(all_patterns) - 1)
            shuffle(all_patterns, p_obj=p)
            p.delete()
        # else {0, 1}: don't shuffle `all_patterns`

        return all_patterns

    def input(self, response_string):
        """ Gets `response_string` from human (CodeMaker), verifies it, takes turn and returns formatted pattern """

        try:  # try to convert `response_string` to tuple (response format)
            response = tuple(
                int(response_peg)
                for response_peg in response_string.strip().split(' ', maxsplit=1)  # only one divide
            )
        except (TypeError, ValueError):
            raise ValueError("Given response is incorrect! Enter again.")

        if not self._validate_response(response):  # check if `response` is correct
            raise ValueError("Given response is incorrect! Enter again.")

        current_pattern = self.take_turn(response)

        if current_pattern is None:  # TODO: delete this section? Return something else?
            return "No further possible solutions."
        else:
            return (
                "My next possible solution is {pattern}.{single}"
                .format(
                    pattern=self._format_pattern(current_pattern),
                    single=self.format_single_poss_sol,
                )
            )

    def take_turn(self, response):
        """ Takes turn as CodeBreaker (with response from CodeMaker) - without response validation, returns pattern """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if self._check_game_end(response):
            return None

        self._turns_counter += 1  # prepare for next turn

        return self._solver.mode_take_turn(response)

    def _check_game_end(self, response):
        """ Checks if the game should end (after current turn) """

        if super()._check_game_end(response):
            return True

        if self._solver.mode_check_game_end():  # check if exists another possible solution
            self._game_status = 3  # no possible solution
            return True

        return False


class MastermindSolverMode1:
    """ ... """

    def __init__(self, upper):
        """ ... """

        self.super = upper  # TODO: is it OK?

        self._turns = dict()  # initialize dictionary of turns
        self._gen_state = self._poss_sol_generator()  # initialize possible solutions generator
        self._second_poss_sol = None  # TODO: temporary
        self._current_poss_sol = self.mode_next_poss_sol()  # get first possible solution

    @property
    def mode_current_poss_sol(self):
        """ ... """

        return self._current_poss_sol

    @property
    def mode_poss_sol_number(self):
        """ ... """

        raise NotImplementedError("It is impossible to calculate possible solutions number in this mode!")

    @property
    def _poss_sol_percent(self):
        """ Returns current possible solution index percentage value """

        return 100 * self._poss_sol_counter / self.super.patterns_number

    def mode_take_turn(self, response):
        """ ... """  # TODO: desc

        self._turns[self._current_poss_sol] = response  # add this turn to the turns dictionary

        self._current_poss_sol = self.mode_next_poss_sol()  # get next possible solution
        return self._current_poss_sol

    def mode_check_game_end(self):
        """ ... """

        return self._second_poss_sol is None

    def _poss_sol_generator(self):
        """ Yields the first pattern that can be a solution based on all previous turns """

        self._poss_sol_counter = 0  # initialize possible solutions counter

        poss_sols = self.super.get_patterns_list()  # TODO: progress tests

        p = Progress("Thinking...", self.super.patterns_number)
        for poss_sol in poss_sols:  # TODO: progress
            self._poss_sol_counter += 1
            p.item()  # TODO: repair it

            if self._mode_check_poss_sol(poss_sol):
                print(
                    "(MODE 1) Found possible solution.",
                    "It's index is {index} of {all} overall ({percent:.2f}%)."
                    .format(
                        index=self._poss_sol_counter,
                        all=self.super.patterns_number,
                        percent=self._poss_sol_percent,
                    )
                )
                yield poss_sol  # yields pattern if it can be a solution

        # after yield the last pattern
        p.delete()
        print(
            "(MODE 1) Finished searching for possible solutions. Nothing was found.",
            "Reached index {index} of {all} overall ({percent:.2f}%)."
            # should be always 100.00%
            .format(
                index=self._poss_sol_counter,
                all=self.super.patterns_number,
                percent=self._poss_sol_percent,
            )
        )

    def _mode_check_poss_sol(self, poss_sol):
        """ Checks if given possible solution still can be a solution based on all previous turns """

        return all(
            self.super.calculate_response(turn_pattern, poss_sol) == turn_response
            for turn_pattern, turn_response in self._turns.items()
        )

    def mode_next_poss_sol(self):
        """ Returns next possible solution (in MODE 1) """

        self.super._single_poss_sol = False  # reset the flag

        # check if previously found possible solution still can be a solution
        if self._second_poss_sol is not None and self._mode_check_poss_sol(self._second_poss_sol):
            # TODO: change `if` criteria (especially when `_second_poss_sol` will be disabled)
            print("(MODE 1) Previously found second possible solution still can be a solution.")
            current = self._second_poss_sol  # yes -> save it as current
        else:
            print("(MODE 1) Searching for possible solution...")
            try:
                current = next(self._gen_state)  # no -> get another possible solution
            except StopIteration:  # there is no solution
                self.super._game_status = 3
                self._second_poss_sol = None
                return None

        print("(MODE 1) Searching for second possible solution...")
        try:
            self._second_poss_sol = next(self._gen_state)  # get second possible solution
        except StopIteration:  # there is no second solution -> only one solution!
            self.super._single_poss_sol = True  # change the flag
            self._second_poss_sol = None

        return current


class MastermindSolverMode2:
    """ ... """

    def __init__(self, upper):
        """ ... """

        self.super = upper  # TODO: is it OK?

        self._poss_sol_list = self.super.get_patterns_list()  # get list of all possible solutions to be filtered
        self._current_poss_sol = self.mode_next_poss_sol()  # get first possible solution

    @property
    def mode_current_poss_sol(self):
        """ ... """

        return self._current_poss_sol

    @property
    def mode_poss_sol_number(self):
        """ ... """

        return len(self._poss_sol_list)

    def mode_take_turn(self, response):
        """ ... """

        # TODO: progress tests
        old_number = self.mode_poss_sol_number

        p = Progress("(MODE 2) Filtering patterns list...", old_number)

        # TODO: maybe remove items from list that doesn't meet condition?
        self._poss_sol_list = [  # filter the existing list
            pattern
            for pattern in self._poss_sol_list
            if p.item(self.super.calculate_response(self._current_poss_sol, pattern) == response)
        ]
        p.delete()

        new_number = self.super.poss_sol_number
        print(
            "(MODE 2) Number of possible solutions is now {new} of {old} (rejected {percent:.2f}% of patterns)."
            .format(
                new=new_number,
                old=old_number,
                percent=100 * (1 - new_number / old_number),
            )
        )

        self._current_poss_sol = self.mode_next_poss_sol()  # get next possible solution
        return self._current_poss_sol

    def mode_check_game_end(self):
        """ ... """

        return self.mode_poss_sol_number <= 1

    def mode_next_poss_sol(self):
        """ Returns next possible solution (in MODE 2) """

        number = self.mode_poss_sol_number
        self.super._single_poss_sol = (number == 1)  # set the flag

        if number:
            return self._poss_sol_list[0]  # take first possible solution from the list
            # TODO: maybe random value? Not always 0? - parameter
        else:
            self.super._game_status = 3
            return None
