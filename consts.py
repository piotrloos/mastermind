########################################
# My version of famous game Mastermind #
# consts.py                            #
# CONSTs for mastermind                #
#             Piotr Loos (c) 2019-2020 #
########################################

from abc import ABCMeta
from solver1 import MastermindSolver1
from solver2 import MastermindSolver2


class Consts(metaclass=ABCMeta):
    """ Namespace for all consts (without instantiating) """

    COLORS_NUMBER = 6               # default number of colors
    COLORS_NUMBER_MAX = 12          # max number of colors

    PEGS_NUMBER = 4                 # default number of pegs
    PEGS_NUMBER_MAX = 10            # max number of pegs

    TURNS_LIMIT = 12                # default turns limit number
    TURNS_LIMIT_MAX = 32            # max turns limit number

    SOLVERS = {
        1: MastermindSolver1,       # patterns checking generator Solver
        2: MastermindSolver2,       # patterns list filtering Solver
    }

    SOLVER_INDEX = 1                # default solver index (one from Solvers list above)

    SHUFFLE_BEFORE = False          # default patterns shuffle before building list setting
    SHUFFLE_AFTER = False           # default patterns shuffle after building list setting
    PROGRESS_TIMING = True          # default `progress_timing` setting flag
    SOLVER1_SECOND_SOLUTION = True  # default `solver1_second_solution` setting flag
    SOLVER2_RANDOM_PATTERN = False  # default `solver2_random_pattern` setting flag
