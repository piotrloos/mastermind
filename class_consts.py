############################################
# My version of the famous Mastermind game #
# class_consts.py                          #
# Constants for mastermind                 #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from abc import ABCMeta


class Consts(metaclass=ABCMeta):
    """ Namespace for all consts (without instantiating) """

    class ColorsNumber(metaclass=ABCMeta):
        type = int
        name = "number of colors"
        min_value = 2
        max_value = 9
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
        name = "number of turns_list limit"
        min_value = 0
        max_value = 32
        default_value = 12
        ask_if_not_given = False

    class ChosenSolver(metaclass=ABCMeta):
        type = int
        name = "chosen Solver number - #1: patterns checking generator Solver, #2: patterns list filtering Solver"
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

    class ShuffleColorsBeforeBuild(metaclass=ABCMeta):
        type = bool
        name = "shuffle colors before patterns list building"
        default_value = False
        ask_if_not_given = False

    class ShufflePatternsAfterBuild(metaclass=ABCMeta):
        type = bool
        name = "shuffle patterns after patterns list building"
        default_value = False
        ask_if_not_given = False

    class ProgressTiming(metaclass=ABCMeta):
        type = bool
        name = "enable progress timing"
        default_value = True
        ask_if_not_given = False

    class Solver1Calc2ndSolution(metaclass=ABCMeta):
        type = bool
        name = "calculate 2nd solution for Solver1"
        default_value = True
        ask_if_not_given = False

    class Solver2TakeRandomPattern(metaclass=ABCMeta):
        type = bool
        name = "take random pattern for Solver2"
        default_value = False
        ask_if_not_given = False

    class ColoredPrints(metaclass=ABCMeta):
        type = bool
        name = "enable terminal printing in color"
        default_value = False
        ask_if_not_given = False
