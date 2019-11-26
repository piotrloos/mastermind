###
# My version of famous game Mastermind
# mastermind.py
# Main file
###

from random import randint
from settings import PEGS, COLORS


class Game:
    """ Game class contains whole game, the pattern and the tries """
    def __init__(self, code=None):
        # check if code is given, if not -> randomize new set of pegs
        if code is None:
            self.pattern = (randint(1, COLORS) for _ in range(PEGS))
        else:
            # check if given code is correct
            if not isinstance(code, tuple) or len(code) != PEGS or any(not isinstance(peg, int) or peg < 1 or peg > COLORS for peg in code):
                raise ValueError("Incorrect code.")
            self.pattern = code
        self.tries = {}  # initialize dict of tries
        self.reveal()  # reveal pattern after successful creation Game class object

    def reveal(self):
        """ Method for returning pattern """
        return self.pattern
