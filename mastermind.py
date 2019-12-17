########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main class file                      #
#                  Piotr Loos (c) 2019 #
########################################

from random import randint, sample
from settings import COLORS, PEGS, MAX_TRIES


class Mastermind:
    """ Mastermind class contains whole game, the solution pattern and the guesses """

    def __init__(self, colors=COLORS, pegs=PEGS, max_tries=MAX_TRIES):
        """ Method for preparing new game with given settings """

        # check if given colors number is correct
        if colors in range(2, 11):  # from 2 to 10
            self.colors = colors
        else:
            raise ValueError("Incorrect number of colors.")

        # check if given pegs number is correct
        if pegs in range(2, 13):  # from 2 to 12
            self.pegs = pegs
        else:
            raise ValueError("Incorrect number of pegs.")

        # check if given max_tries number is correct
        if max_tries in range(1, 33):  # from 1 to 32
            self.max_tries = max_tries
        else:
            raise ValueError("Incorrect number of max_tries.")

        self.guesses = dict()  # initialize dictionary of guesses
        self.colors_set = set(range(self.colors))  # initialize set of colors (for performance)
        self.solution = None
        self.counter = 1  # initialize tries counter
        self.status = 0  # 0 = game is active, 1 = solution is found, 2 = reached tries limit, 3 = no possible solution
        self.hint_number = self.colors ** self.pegs  # calculate number of all possible patterns

    def calculate(self, pattern1, pattern2=None):
        """ Method for calculating black and white pegs from guess pattern """

        # there is a possibility to calculate pattern relative to another pattern, not always solution
        if pattern2 is None:
            if self.solution is None:
                raise ValueError("No solution pattern to calculate.")
            else:
                pattern2 = self.solution

        # black_pegs defines how many guess pegs are in proper color and in proper location
        black_pegs = sum(peg1 == peg2 for peg1, peg2 in zip(pattern1, pattern2))

        # white_black_pegs defines how many guess pegs are in proper color regardless to location
        # white_pegs defines how many guess pegs are in proper color and wrong location
        # to calculate white_pegs it's needed to subtract black_pegs from white_black_pegs
        white_black_pegs = sum(min(pattern1.count(peg), pattern2.count(peg)) for peg in self.colors_set)

        return black_pegs, white_black_pegs - black_pegs  # return tuple with black and white pegs

    def check_end_criteria(self, result):
        """ Method for checking if the game should end """

        if result == (self.pegs, 0):  # check if the pattern is guessed correctly
            self.status = 1
            return True
        else:
            self.counter += 1  # prepare for next turn

        if self.counter > self.max_tries:  # check if the player still can guess
            self.status = 2
            return True

        return False

    @staticmethod
    def print_pattern(pattern):
        """ Method for formatting pattern """

        return "[ " + " ".join(chr(peg + 97) for peg in pattern) + " ]"


class Game(Mastermind):
    """ Game class inherits from Mastermind class """

    def __init__(self, solution=None, **kwargs):
        """ Method for initializing Game class object """

        super().__init__(**kwargs)  # initialize Mastermind class object

        # check if solution is given, if not -> randomize new pattern
        if solution is None:
            self.solution = tuple(randint(0, self.colors - 1) for _ in range(self.pegs))
        else:
            # check if given solution is correct
            if self.validate_pattern(solution):
                self.solution = solution
            else:
                raise ValueError("Incorrect solution pattern.")

        self.last_pattern = None

    def input_pattern(self, pattern_string):
        """ Method for inputting pattern from player """

        try:  # try to convert pattern_string to tuple (pattern format)
            pattern = tuple(ord(peg) - 97 for peg in pattern_string.split(maxsplit=self.pegs - 1))
        except ValueError:
            return None  # there was an error

        if self.validate_pattern(pattern):  # check if pattern is correct
            self.last_pattern = pattern
            return self.add_pattern(pattern)  # OK
        else:
            return None  # there was an error

    def validate_pattern(self, pattern):
        """ Method for validating given pattern """

        return isinstance(pattern, tuple) and len(pattern) == self.pegs and all(
            peg in self.colors_set for peg in pattern)

    def add_pattern(self, pattern):
        """ Method for adding pattern by the player """

        if pattern in self.guesses.keys():  # check if given pattern was already calculated
            result = self.guesses[pattern]  # retrieve result from dictionary
        else:
            result = self.calculate(pattern)  # calculate the result
            self.guesses[pattern] = result  # save the result to the dictionary

        self.check_end_criteria(result)
        return result

    def prompt(self):
        """ Method for returning prompt string """

        return "{}: ".format(self.counter)


class Helper(Mastermind):
    """ Helper class inherits from Mastermind class """

    def __init__(self, hint_mode=1, **kwargs):
        """ Method for initializing Helper class object """

        super().__init__(**kwargs)  # initialize Mastermind class object

        # check if given hint_mode is correct
        if hint_mode in range(0, 3):  # from 0 to 2
            self.hint_mode = hint_mode
        else:
            raise ValueError("Incorrect hints shuffle mode.")

        self.hint = self.hint_generator()  # initialize hint pattern generator
        self.current_pattern = self.hint_next()  # get first pattern
        self.next_pattern = self.hint_next(set_status=False)  # get second pattern

    def input_result(self, result_string):
        """ Method for inputting result from player """

        try:  # try to convert result_string to tuple (result format)
            result = tuple(int(result_peg) for result_peg in result_string.split(maxsplit=1))
        except ValueError:
            return True  # there was an error

        if self.validate_result(result):  # check if result is correct
            self.add_result(result)
            return False  # OK
        else:
            return True  # there was an error

    def validate_result(self, result):
        """ Method for validating given result """

        return isinstance(result, tuple) and len(result) == 2 and all(
            peg in range(0, self.pegs + 1) for peg in [result[0], result[1], result[0] + result[1]]
        )

    def add_result(self, result):
        """ Method for adding result by the player """

        self.guesses[self.current_pattern] = result

        if not self.check_end_criteria(result):
            self.queue_next_pattern()

    def hint_generator(self):
        """ Method for yielding the first pattern that could be the solution based on all previous guesses """

        # generate all possible patterns using my own function
        # it's similar to Cartesian product (import itertools.product),
        # but operates on tuples (not lists) and works direct on Mastermind variables

        patterns = (),  # initialize with tuple containing empty tuple

        # build list (generator) of all possible patterns
        if self.hint_mode == 1:  # shuffle set of colors to build patterns from (on every iteration)
            for _ in range(self.pegs):
                patterns = ((*pattern, peg) for pattern in patterns for peg in sample(self.colors_set, self.colors))
        else:  # no shuffle patterns list, they will be in ascending order
            for _ in range(self.pegs):
                patterns = ((*pattern, peg) for pattern in patterns for peg in self.colors_set)

        if self.hint_mode == 2:  # shuffle all patterns set (at once)
            patterns_set = set(patterns)
            patterns = sample(patterns_set, len(patterns_set))  # now patterns are list, not generator

        hint_counter = 0
        length = len(str(self.hint_number))

        for hint_pattern in patterns:
            hint_counter += 1

            if self.hint_check(hint_pattern):
                print("{:>{l}d} / {:>{l}d} ({:6.2f}%)".format(hint_counter, self.hint_number, 100 * hint_counter/self.hint_number, l=length))
                yield hint_pattern  # yields pattern if it can be a solution
        print("{:>{l}d} / {:>{l}d} ({:6.2f}%)".format(hint_counter, self.hint_number, 100 * hint_counter / self.hint_number, l=length))

    def hint_check(self, hint_pattern):
        """ Method for checking if given pattern can be a hint based on all previous guesses """

        return all(self.guesses[pattern] == self.calculate(pattern, hint_pattern) for pattern in self.guesses.keys())

    def hint_next(self, set_status=True):
        """ Method for getting the next hint pattern """

        try:
            return next(self.hint)
        except StopIteration:
            if set_status:
                self.status = 3
            return None

    def queue_next_pattern(self):
        """ Method for generating the next hint pattern and checking if exists another solution """

        if self.next_pattern is None:
            self.status = 3
            return
        else:
            if self.hint_check(self.next_pattern):
                self.current_pattern = self.next_pattern
            else:
                self.current_pattern = self.hint_next()

        self.next_pattern = self.hint_next(set_status=False)

        if self.current_pattern is not None and self.next_pattern is None:
            print("Only one possible pattern!")  # for tests

    def prompt(self):
        """ Method for returning prompt string """

        return "{}: {} -> ".format(self.counter, self.print_pattern(self.current_pattern))
