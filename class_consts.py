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
        name = "colors_number"
        desc = "set number of different pegs colors"
        min_value = 2
        max_value = 24
        default_value = 6
        ask_if_not_given = True

    class PegsNumber(metaclass=ABCMeta):
        type = int
        name = "pegs_number"
        desc = "set number of pegs in every pattern"
        min_value = 2
        max_value = 16
        default_value = 4
        ask_if_not_given = True

    class TurnsLimit(metaclass=ABCMeta):
        type = int
        name = "turns_limit"
        desc = "set number of turns allowed in every game"
        min_value = 0
        max_value = 32
        default_value = 12
        ask_if_not_given = False

    class UseDigitsForColors(metaclass=ABCMeta):
        type = bool
        name = "use_digits_for_colors"
        desc = "True = uses digits from 1-10 (digit 0 means 10) and then letters, False = uses only letters"
        default_value = True
        ask_if_not_given = False

    class ChosenSolver(metaclass=ABCMeta):
        type = int
        name = "chosen_solver"
        desc = "choose Solver - #1: patterns checking generator Solver, #2: patterns list filtering Solver"
        min_value = 1
        max_value = 2
        default_value = 1
        ask_if_not_given = False

    class UseItertools(metaclass=ABCMeta):
        type = bool
        name = "use_itertools"
        desc = "enable using built-in itertools product function to generate patterns"
        default_value = True
        ask_if_not_given = False

    class PreBuildPatterns(metaclass=ABCMeta):
        type = bool
        name = "pre_build_patterns"
        desc = "enable pre-building list of all possible patterns"
        default_value = False
        ask_if_not_given = False

    class ShuffleColorsBeforeBuild(metaclass=ABCMeta):
        type = bool
        name = "shuffle_colors_before_build"
        desc = "enable shuffling colors before patterns list building"
        default_value = False
        ask_if_not_given = False

    class ShuffleColorsDuringBuild(metaclass=ABCMeta):
        type = bool
        name = "shuffle_colors_during_build"
        desc = "enable shuffling colors during patterns list building"
        default_value = False
        ask_if_not_given = False

    class ShufflePatternsAfterBuild(metaclass=ABCMeta):
        type = bool
        name = "shuffle_patterns_after_build"
        desc = "enable shuffling patterns after patterns list building"
        default_value = False
        ask_if_not_given = False

    class ProgressTiming(metaclass=ABCMeta):
        type = bool
        name = "progress_timing"
        desc = "enable timing of progress operations"
        default_value = True
        ask_if_not_given = False

    class Solver1Calc2ndSolution(metaclass=ABCMeta):
        type = bool
        name = "solver1_calc_2nd_solution"
        desc = "enable calculating 2nd possible solution for Solver1"
        default_value = True
        ask_if_not_given = False

    class Solver2TakeRandomPattern(metaclass=ABCMeta):
        type = bool
        name = "solver2_take_random_pattern"
        desc = "enable taking random pattern from the list for Solver2"
        default_value = False
        ask_if_not_given = False

    class Solver2PrintPossibleSolutionsThreshold(metaclass=ABCMeta):
        type = int
        name = "solver2_print_possible_solutions_threshold"
        desc = "set threshold for printing remaining possible solutions for Solver2 (0 = disabled)"
        min_value = 0
        max_value = 100
        default_value = 10
        ask_if_not_given = False

    class ColoredPrints(metaclass=ABCMeta):
        type = bool
        name = "colored_prints"
        desc = "enable terminal printings in color"
        default_value = False
        ask_if_not_given = False

    class PrintTurnsList(metaclass=ABCMeta):
        type = bool
        name = "print_turns_list"
        desc = "enable printing turns list after each turn"
        default_value = True
        ask_if_not_given = False
