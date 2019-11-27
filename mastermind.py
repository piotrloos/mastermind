########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main file                            #
########################################

from random import randint
from settings import PEGS, COLORS


class Game:
    """ Game class contains whole game, the pattern and the tries """
    def __init__(self, pattern=None, pegs=PEGS, colors=COLORS):

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

        # check if pattern is given, if not -> randomize new pattern
        if pattern is None:
            self.pattern = tuple(randint(1, self.colors) for _ in range(self.pegs))
        else:
            # check if given pattern is correct
            if self.validate_pattern(pattern):
                self.pattern = pattern
            else:
                raise ValueError("Incorrect pattern.")

        self.guesses = {}  # initialize dict of guesses
        print(self.reveal_pattern())  # reveal pattern after successful creation Game class object

    def validate_pattern(self, pattern):
        return isinstance(pattern, tuple) and len(pattern) == self.pegs and all(
            peg in range(1, self.colors + 1) for peg in pattern)

    def reveal_pattern(self):
        """ Method for returning pattern """
        return self.pattern
