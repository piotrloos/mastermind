############################################
# My version of the famous Mastermind game #
# class_consts.py                          #
# Constants for mastermind                 #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from abc import ABCMeta


class Consts(metaclass=ABCMeta):
    """ Namespace for all consts (without instantiating) """

    # TERMINAL SETTINGS

    class StyledPrints(metaclass=ABCMeta):
        name = "styled_prints"
        desc = "enable advanced terminal styles for prints (color, bold, underline etc.)"
        type = bool
        default_value = True
        ask_if_not_given = True

    class UseDigitsForColors(metaclass=ABCMeta):
        name = "use_digits_for_colors"
        desc = "True = use digits from 1-10 (digit 0 means 10) and then letters, False = use only letters"
        type = bool
        default_value = True
        ask_if_not_given = False

    # TODO: add new `use_progress` bool setting

    class ProgressTiming(metaclass=ABCMeta):
        name = "progress_timing"
        desc = "enable timing of Progress operations"
        type = bool
        default_value = True
        ask_if_not_given = False

    class PrintGuessesList(metaclass=ABCMeta):
        name = "print_guesses_list"
        desc = "enable printing guesses list after each guess"
        type = bool
        default_value = True
        ask_if_not_given = False

    # MASTERMIND SETTINGS

    class PegColors(metaclass=ABCMeta):
        name = "peg_colors"
        desc = "set number of different pegs colors"
        type = int
        min_value = 2
        max_value = 24
        default_value = 6
        ask_if_not_given = True

    class PegsInPattern(metaclass=ABCMeta):
        name = "pegs_in_pattern"
        desc = "set number of pegs in every pattern"
        type = int
        min_value = 2
        max_value = 16
        default_value = 4
        ask_if_not_given = True

    class AllowBlanks(metaclass=ABCMeta):
        name = "allow_blanks"
        desc = "enable blank pegs in guesses (not in solution)"
        type = bool
        default_value = False
        ask_if_not_given = False

    class AllowDuplicates(metaclass=ABCMeta):
        name = "allow_duplicates"
        desc = "enable duplicating pegs of the same colors in patterns (guesses and solution)"
        type = bool
        default_value = True
        ask_if_not_given = False

    class GuessesLimit(metaclass=ABCMeta):
        name = "guesses_limit"
        desc = "set number of guesses allowed in every game (0 = unlimited)"
        type = int
        min_value = 0
        max_value = 32
        default_value = 12
        ask_if_not_given = False

    # SOLVING SETTINGS

    class ChosenSolver(metaclass=ABCMeta):
        name = "chosen_solver"
        desc = "choose Solver: #1 = patterns checking generator Solver, #2 = patterns list filtering Solver"
        type = int
        min_value = 1
        max_value = 2
        default_value = 1
        ask_if_not_given = False

    class PreBuildPatterns(metaclass=ABCMeta):
        name = "pre_build_patterns"
        desc = "enable pre-building list of all possible patterns"
        type = bool
        default_value = False
        ask_if_not_given = False

    class UseItertoolsForBuild(metaclass=ABCMeta):
        name = "use_itertools_for_build"
        desc = "enable using built-in itertools product function to generate patterns"
        type = bool
        default_value = True
        ask_if_not_given = False

    class ShuffleColorsBeforeBuild(metaclass=ABCMeta):
        name = "shuffle_colors_before_build"
        desc = "enable shuffling colors before patterns list building"
        type = bool
        default_value = False
        ask_if_not_given = False

    class ShuffleColorsDuringBuild(metaclass=ABCMeta):
        name = "shuffle_colors_during_build"
        desc = "enable shuffling colors during patterns list building"
        type = bool
        default_value = False
        ask_if_not_given = False

    class ShufflePatternsAfterBuild(metaclass=ABCMeta):
        name = "shuffle_patterns_after_build"
        desc = "enable shuffling patterns after patterns list building"
        type = bool
        default_value = False
        ask_if_not_given = False

    # SOLVER #1 SETTINGS

    class Solver1Calc2ndSolution(metaclass=ABCMeta):
        name = "solver1_calc_2nd_solution"
        desc = "enable calculating 2nd possible solution for Solver1"
        type = bool
        default_value = True
        ask_if_not_given = False

    # SOLVER #2 SETTINGS

    class Solver2TakeRandomPattern(metaclass=ABCMeta):
        name = "solver2_take_random_pattern"
        desc = "enable taking random pattern from the list for Solver2"
        type = bool
        default_value = False
        ask_if_not_given = False

    class Solver2PrintPossibleSolutionsThreshold(metaclass=ABCMeta):
        name = "solver2_print_possible_solutions_threshold"
        desc = "set threshold for printing remaining possible solutions for Solver2 (0 = disabled)"
        type = int
        min_value = 0
        max_value = 100
        default_value = 10
        ask_if_not_given = False
