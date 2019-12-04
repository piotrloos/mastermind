########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main class file                      #
#                  Piotr Loos (c) 2019 #
########################################

from random import randint, sample
from settings import PEGS, COLORS, MAX_TRIES
# from itertools import product


class Mastermind:
    """ Mastermind class contains whole game, the solution pattern and the guesses """

    def __init__(self, solution=None, generate=True, pegs=PEGS, colors=COLORS, max_tries=MAX_TRIES):
        """ Method for preparing new game with given settings """

        # check if given pegs number is correct
        if pegs in range(2, 9):  # from 2 to 8
            self.pegs = pegs
        else:
            raise ValueError("Incorrect number of pegs.")

        # check if given colors number is correct
        if colors in range(2, 11):  # from 2 to 10
            self.colors = colors
        else:
            raise ValueError("Incorrect number of colors.")

        # check if given max_tries number is correct
        if max_tries in range(1, 33):  # from 1 to 32
            self.max_tries = max_tries
        else:
            raise ValueError("Incorrect number of max_tries.")

        # check if solution is given, if not -> randomize new pattern (if needed)
        if solution is None:
            if generate:
                self.solution = tuple(randint(1, self.colors) for _ in range(self.pegs))
            else:
                self.solution = None
        else:
            # check if given solution is correct
            if self.validate_pattern(solution):
                self.solution = solution
            else:
                raise ValueError("Incorrect solution pattern.")

        self.guesses = dict()  # initialize dictionary of guesses
        self.colors_set = set(range(1, self.colors + 1))  # initialize set of colors (for performance)
        self.tries_counter = 1  # initialize tries counter
        self.active = True  # initialize flag which indicates whether game is active
        self.won = False  # initialize flag which indicates whether the player correctly guessed the solution

    def input_pattern(self, pattern_string):
        """ Method for inputting pattern from player """

        try:
            pattern = tuple(int(peg) for peg in pattern_string.split(maxsplit=self.pegs - 1))
        except ValueError:
            return None

        if self.validate_pattern(pattern):
            return pattern
        else:
            return None

    def validate_pattern(self, pattern):
        """ Method for validating given pattern """

        return isinstance(pattern, tuple) and len(pattern) == self.pegs and all(
            peg in self.colors_set for peg in pattern)

    def input_result(self, result_string):
        """ Method for inputting result from player """

        try:
            result = tuple(int(peg) for peg in result_string.split(maxsplit=1))
        except ValueError:
            return None

        if self.validate_result(result):
            return result
        else:
            return None

    def validate_result(self, result):
        """ Method for validating given result """

        return isinstance(result, tuple) and len(result) == 2 and all(
            peg in range(0, self.colors + 1) for peg in [result[0], result[1], result[0] + result[1]])

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

    def guess(self, pattern):
        """ Method for guessing pattern by the player """

        if pattern in self.guesses.keys():  # check if given pattern was already calculated
            result = self.guesses[pattern]  # retrieve result from dictionary
        else:
            result = self.calculate(pattern)  # calculate the result
            self.guesses[pattern] = result  # save the result to the dictionary

        if result == (self.pegs, 0):  # check if the pattern is guessed correctly
            self.active = False
            self.won = True
        else:
            self.tries_counter += 1

        if self.tries_counter > self.max_tries:  # check if the player still can guess
            self.active = False

        return result

    def hint_generator(self, shuffle=True):
        """ Method for yielding the first pattern that could be the solution based on all previous guesses """

        # generate all possible patterns using my own function
        # it's similar to Cartesian product (from itertools import product),
        # but operates on tuples (not lists) and works direct on Mastermind variables

        patterns = [[]]

        if shuffle:
            for _ in range(self.pegs):
                patterns = ((*x, y) for x in patterns for y in sample(self.colors_set, self.colors))
        else:
            for _ in range(self.pegs):
                patterns = ((*x, y) for x in patterns for y in self.colors_set)

        # for hint_pattern in product(self.colors_set, repeat=self.pegs):
        for hint_pattern in patterns:

            # check all previous guesses and their result comparing to hint_pattern
            if all(self.guesses[pattern] == self.calculate(pattern, hint_pattern)
                   for pattern in self.guesses.keys()
                   ):
                yield hint_pattern  # yields pattern if it can be a solution

    def reveal_solution(self):
        """ Method for returning solution pattern """

        self.active = False
        return self.solution
