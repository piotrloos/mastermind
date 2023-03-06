############################################
# My version of the famous Mastermind game #
# class_settings.py                        #
# Mastermind settings file                 #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_components import peg_class, pattern_class, response_class, turn_class, turns_list_class
from class_consts import Consts
from class_colors import Color, NoColor
from class_solver1 import MastermindSolver1
from class_solver2 import MastermindSolver2
from itertools import product


class Settings:
    """ Class for all the game settings """

    def __init__(
            self,
            *args,
            colors_number=None,
            pegs_number=None,
            turns_limit=None,
            chosen_solver=None,
            use_itertools=None,
            pre_build_patterns=None,
            shuffle_colors_before_build=None,
            shuffle_patterns_after_build=None,
            progress_timing=None,
            solver1_calc_2nd_solution=None,
            solver2_take_random_pattern=None,
            colored_prints=None,
            **kwargs,
    ):
        """ Initializes `Settings` class object """

        self._colors_number = self._get_setting(Consts.ColorsNumber, colors_number)
        self._pegs_number = self._get_setting(Consts.PegsNumber, pegs_number)
        self._turns_limit = self._get_setting(Consts.TurnsLimitNumber, turns_limit)
        self._chosen_solver = self._get_setting(Consts.ChosenSolver, chosen_solver)
        self._use_itertools = self._get_setting(Consts.UseItertools, use_itertools)
        self._pre_build_patterns = self._get_setting(Consts.PreBuildPatterns, pre_build_patterns)
        self._shuffle_colors_before_build = self._get_setting(Consts.ShuffleColorsBeforeBuild, shuffle_colors_before_build)
        self._shuffle_patterns_after_build = self._get_setting(Consts.ShufflePatternsAfterBuild, shuffle_patterns_after_build)
        self._progress_timing = self._get_setting(Consts.ProgressTiming, progress_timing)
        self._solver1_calc_2nd_solution = self._get_setting(Consts.Solver1Calc2ndSolution, solver1_calc_2nd_solution)
        self._solver2_take_random_pattern = self._get_setting(Consts.Solver2TakeRandomPattern, solver2_take_random_pattern)
        self._colored_prints = self._get_setting(Consts.ColoredPrints, colored_prints)

        if self._colored_prints:
            self.color = Color()
        else:
            self.color = NoColor()

        self._solvers = {
            1: MastermindSolver1,  # patterns checking generator Solver
            2: MastermindSolver2,  # patterns list filtering Solver
        }

        for attribute in args:
            print(
                f"{self.color.error_on}"
                f"[Settings] Attribute "
                f"{self.color.attribute_on}"
                f"{attribute}"
                f"{self.color.attribute_off}"
                f" has not been recognized! Ignoring."
                f"{self.color.error_off}"
            )

        for key, value in kwargs.items():
            print(
                f"{self.color.error_on}"
                f"[Settings] Keyword "
                f"{self.color.attribute_on}"
                f"{key}"
                f"{self.color.attribute_off}"
                f" and it's value "
                f"{self.color.attribute_on}"
                f"{value}"
                f"{self.color.attribute_off}"
                f" has not been recognized! Ignoring."
                f"{self.color.error_off}"
            )

        self.Peg = peg_class(self)
        self.Pattern = pattern_class(self)
        self.Response = response_class(self)
        self.Turn = turn_class(self)
        self.TurnsList = turns_list_class(self)

        if self._pre_build_patterns:
            self._all_patterns_list = self.Pattern.build_patterns()  # build all patterns list (once for several games)
        else:
            if self._use_itertools:
                # get `itertools.product` generator
                self._all_patterns_gen = map(lambda pattern_tuple: self.Pattern(pattern_tuple),
                                             product(self.Peg.all_colors_list, repeat=self._pegs_number))
            else:
                # get reference for my generator (without call)
                self._all_patterns_gen = self.Pattern.gen_patterns

        print()

    @staticmethod
    def _get_setting(setting, value):
        """ Returns validated value (given as a parameter or inputted by user) for setting """

        if setting.type is bool:
            values_to_check = {0, 1}
            values_to_print = "0/False or 1/True"
        elif setting.type is int:
            values_to_check = range(setting.min_value, setting.max_value + 1)
            values_to_print = f"from {setting.min_value} to {setting.max_value}"
        else:
            raise TypeError(
                f"[Settings] Setting type `{setting.type}` for `{setting.name}` is incorrect!"
            )

        if setting.default_value not in values_to_check:
            raise ValueError(
                f"[Settings] Default `{setting.name}` value ({setting.default_value}) is incorrect!"
            )

        parameter_flag = True
        value_str = ""

        while value not in values_to_check:

            if parameter_flag:
                if value is not None:
                    print(
                        f"[Settings] Given `{setting.name}` value ({value}) as a parameter is incorrect!"
                    )
            else:
                print(
                    f"[Settings] Entered `{setting.name}` value ({value_str}) is incorrect!"
                )

            if not setting.ask_if_not_given:
                # print(
                #     f"Taking default `{setting.name}` value ({setting.default_value})."
                # )
                value = setting.default_value
            else:
                parameter_flag = False
                value_str = input(
                    f"[Settings] Enter `{setting.name}` value ({values_to_print}), "
                    f"leave empty for default value ({setting.default_value}): "
                ).strip()

                if value_str == "":
                    print(
                        f"[Settings] Nothing entered. Taking default `{setting.name}` value ({setting.default_value})."
                    )
                    value = setting.default_value
                elif setting.type is bool and value_str.lower() in {"0", "false", "f", "no", "n", "x", "-"}:
                    print(
                        f"[Settings] Entered value `{value_str}` for `{setting.name}` recognized as `False`."
                    )
                    value = 0
                elif setting.type is bool and value_str.lower() in {"1", "true", "t", "yes", "y", "v", "+"}:
                    print(
                        f"[Settings] Entered value `{value_str}` for `{setting.name}` recognized as `True`."
                    )
                    value = 1
                else:
                    try:
                        value = int(value_str)
                    except ValueError:
                        value = value_str

        # TODO: create property for setting

        return setting.type(value)

    @property
    def colors_number(self):
        """ Returns number of colors """

        return self._colors_number

    @property
    def pegs_number(self):
        """ Returns number of pegs """

        return self._pegs_number

    @property
    def patterns_number(self):
        """ Returns number of all possible patterns """

        return self._colors_number ** self._pegs_number

    @property
    def turns_limit(self):
        """ Returns turns limit number """

        return self._turns_limit

    @property
    def chosen_solver(self):
        """ Returns chosen solver number """

        return self._chosen_solver

    @property
    def use_itertools(self):
        """ Returns 'use built-in itertools product function to generate patterns """

        return self._use_itertools

    @property
    def pre_build_patterns(self):
        """ Returns 'pre-build all possible patterns list' setting """

        return self._pre_build_patterns

    @property
    def shuffle_colors_before_build(self):
        """ Returns 'shuffle colors before building list' setting """

        return self._shuffle_colors_before_build

    @property
    def shuffle_patterns_after_build(self):
        """ Returns 'shuffle patterns after building list' setting """

        return self._shuffle_patterns_after_build

    @property
    def progress_timing(self):
        """ Returns `progress_timing` setting """

        return self._progress_timing

    @property
    def solver1_calc_2nd_solution(self):
        """ Returns `solver1_calc_2nd_solution` setting (only for Solver1) """

        return self._solver1_calc_2nd_solution

    @property
    def solver2_take_random_pattern(self):
        """ Returns `solver2_take_random_pattern` setting (only for Solver2) """

        return self._solver2_take_random_pattern

    @property
    def colored_prints(self):
        """ Returns `colored_prints` setting """

        return self._colored_prints

    @property
    def all_colors_list_formatted(self):
        """ Returns formatted list of all possible colors """

        return f"{{{','.join(peg.__str__() for peg in self.Peg.all_colors_list)}}}"

    @property
    def all_patterns_list(self):
        """ Returns list of all possible patterns """

        return self._all_patterns_list

    @property
    def all_patterns_gen(self):
        """ Returns generator of all possible patterns """

        return self._all_patterns_gen

    @property
    def solvers(self):
        """ Returns dict containing all defined solvers (in Consts) """

        return self._solvers
