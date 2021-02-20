########################################
# My version of famous game Mastermind #
# consts.py                            #
# CONSTs for mastermind                #
#             Piotr Loos (c) 2019-2021 #
########################################

from abc import ABCMeta


class Consts(metaclass=ABCMeta):
    """ Namespace for all consts (without instantiating) """

    class ColorsNumber(metaclass=ABCMeta):
        type = int
        name = "number of colors"
        min_value = 2
        max_value = 12
        default_value = 6
        ask_if_not_given = True     # if False - take default value without asking user

    class PegsNumber(metaclass=ABCMeta):
        type = int
        name = "number of pegs"
        min_value = 2
        max_value = 10
        default_value = 4
        ask_if_not_given = True

    class TurnsLimitNumber(metaclass=ABCMeta):
        type = int
        name = "number of turns limit"
        min_value = 0
        max_value = 32
        default_value = 12
        ask_if_not_given = False

    class SolverIndex(metaclass=ABCMeta):
        type = int
        name = "solver index"
        min_value = 1
        max_value = 2
        default_value = 1
        ask_if_not_given = False

    class UseItertools(metaclass=ABCMeta):
        type = bool
        name = "use built-in itertools product function to generate patterns"
        default_value = True
        ask_if_not_given = False

    class PreBuildPatterns(metaclass=ABCMeta):
        type = bool
        name = "pre-build list of all possible patterns"
        default_value = False
        ask_if_not_given = False

    class ShufflePatternsBeforeBuilding(metaclass=ABCMeta):
        type = bool
        name = "shuffle patterns before building list"
        default_value = False
        ask_if_not_given = False

    class ShufflePatternsAfterBuilding(metaclass=ABCMeta):
        type = bool
        name = "shuffle patterns after building list"
        default_value = False
        ask_if_not_given = False

    class ProgressTiming(metaclass=ABCMeta):
        type = bool
        name = "enable progress timing"
        default_value = True
        ask_if_not_given = False

    class Solver1SecondSolution(metaclass=ABCMeta):
        type = bool
        name = "enable Solver1 second solution setting"
        default_value = True
        ask_if_not_given = False

    class Solver2RandomPattern(metaclass=ABCMeta):
        type = bool
        name = "enable Solver2 random pattern setting"
        default_value = False
        ask_if_not_given = False

    class ColoredPrints(metaclass=ABCMeta):
        type = bool
        name = "enable printing in color"
        default_value = True
        ask_if_not_given = False
