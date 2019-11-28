########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main class file                      #
########################################

from random import randint
from settings import PEGS, COLORS


class Mastermind:
    """ Mastermind class contains whole game, the solution pattern and the guesses """

    def __init__(self, solution_pattern=None, pegs=PEGS, colors=COLORS):
        """ Method for preparing new game with given settings """

        # check if given pegs number is correct
        if pegs in range(2, 9):  # form 2 to 8
            self.pegs = pegs
        else:
            raise ValueError("Incorrect number of pegs.")

        # check if given colors number is correct
        if colors in range(2, 11):  # from 2 to 10
            self.colors = colors
        else:
            raise ValueError("Incorrect number of colors.")

        # check if solution_pattern is given, if not -> randomize new pattern
        if solution_pattern is None:
            self.solution_pattern = tuple(randint(1, self.colors) for _ in range(self.pegs))
        else:
            # check if given solution_pattern is correct
            if self.validate_pattern(solution_pattern):
                self.solution_pattern = solution_pattern
            else:
                raise ValueError("Incorrect solution pattern.")

        self.guess_dict = {}  # initialize dictionary of guesses
        self.guess_count = 0  # initialize guess counter
        self.game_finished = False  # initialize flag which indicates whether pattern is guessed
        # print(self.reveal_pattern())  # reveal pattern after successful creation Mastermind class object

    def validate_pattern(self, pattern):
        """ Method for validating given pattern """

        return isinstance(pattern, tuple) and len(pattern) == self.pegs and all(
            peg in range(1, self.colors + 1) for peg in pattern)

    def calculate_pattern(self, pattern1, pattern2=None):
        """ Method for calculating black and white pegs from guess pattern """

        # there is a possibility to calculate pattern relative to another pattern, not always solution_pattern
        if pattern2 is None:
            pattern2 = self.solution_pattern

        # black_pegs defines how many guess pegs are in proper color and in proper location
        black_pegs = sum(peg1 == peg2 for peg1, peg2 in zip(pattern1, pattern2))

        # white_black_pegs defines how many guess pegs are in proper color regardless to location
        # white_pegs defines how many guess pegs are in proper color and wrong location
        # to calculate white_pegs it's needed to subtract black_pegs from white_black_pegs
        white_black_pegs = sum(min(pattern1.count(peg), pattern2.count(peg)) for peg in range(1, self.colors + 1))

        return black_pegs, white_black_pegs - black_pegs  # return tuple with black and white pegs

    def guess_pattern(self, guess_pattern):
        """ Method for guessing pattern by the player """

        if not self.validate_pattern(guess_pattern):  # check if given pattern is correct
            raise ValueError("Incorrect guess pattern.")

        self.guess_count += 1  # increment the guess counter

        if guess_pattern not in self.guess_dict:  # check if given pattern was already calculated
            self.guess_dict[guess_pattern] = self.calculate_pattern(guess_pattern)  # save the result to the dictionary
            if self.guess_dict[guess_pattern] == (self.pegs, 0):  # check if the pattern is guessed correctly
                self.game_finished = True

        return self.guess_dict[guess_pattern]

    def hint_pattern(self):
        pass

    def reveal_pattern(self):
        """ Method for returning solution pattern """

        self.game_finished = True
        return self.solution_pattern
