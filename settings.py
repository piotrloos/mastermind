########################################
# My version of famous game Mastermind #
# settings.py                          #
# Mastermind settings file             #
#             Piotr Loos (c) 2019-2020 #
########################################

import components
from consts import Consts
from solver1 import MastermindSolver1
from solver2 import MastermindSolver2


class Settings:
    """ Class for all the game settings """

    def __init__(
            self,
            *args,
            colors_number=None,
            pegs_number=None,
            turns_limit=None,
            solver_index=None,
            pre_build_patterns=None,
            shuffle_before=None,
            shuffle_after=None,
            progress_timing=None,
            solver1_second_solution=None,
            solver2_random_pattern=None,
            **kwargs,
    ):
        """ Initializes `Settings` class object """

        self._colors_number = self._get_setting(Consts.ColorsNumber, colors_number)
        self._pegs_number = self._get_setting(Consts.PegsNumber, pegs_number)
        self._turns_limit = self._get_setting(Consts.TurnsLimitNumber, turns_limit)
        self._solver_index = self._get_setting(Consts.SolverIndex, solver_index)
        self._pre_build_patterns = self._get_setting(Consts.PreBuildPatterns, pre_build_patterns)
        self._shuffle_before = self._get_setting(Consts.ShufflePatternsBeforeBuilding, shuffle_before)
        self._shuffle_after = self._get_setting(Consts.ShufflePatternsAfterBuilding, shuffle_after)
        self._progress_timing = self._get_setting(Consts.ProgressTiming, progress_timing)
        self._solver1_second_solution = self._get_setting(Consts.Solver1SecondSolution, solver1_second_solution)
        self._solver2_random_pattern = self._get_setting(Consts.Solver2RandomPattern, solver2_random_pattern)

        self._solvers = {
            1: MastermindSolver1,  # patterns checking generator Solver
            2: MastermindSolver2,  # patterns list filtering Solver
        }

        for attribute in args:
            print(
                f"Attribute `{attribute}` has not been recognized! Ignoring."
            )

        for key, value in kwargs.items():
            print(
                f"Keyword `{key}` and it's value `{value}` has not been recognized! Ignoring."
            )

        self.Peg = components.peg_class(self)
        self.Colors = components.colors_class(self)  # TODO: delete this class
        self.Pattern = components.pattern_class(self)
        self.Response = components.response_class(self)
        self.Turn = components.turn_class(self)
        self.Turns = components.turns_class(self)

        self._all_colors_list = self.Colors()

        if self._pre_build_patterns:
            self._all_patterns_list = self.Pattern.build_patterns()  # build all patterns list (once for several games)
        else:
            self._all_patterns_gen = self.Pattern.gen_patterns  # get reference for patterns generator (without call)

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
                f"Setting type `{setting.type}` for `{setting.name}` is incorrect!"
            )

        if setting.default_value not in values_to_check:
            raise ValueError(
                f"Default `{setting.name}` value ({setting.default_value}) is incorrect!"
            )

        parameter_flag = True
        value_str = ""

        while value not in values_to_check:

            if parameter_flag:
                if value is not None:
                    print(
                        f"Given `{setting.name}` value ({value}) as a parameter is incorrect!"
                    )
            else:
                print(
                    f"Entered `{setting.name}` value ({value_str}) is incorrect!"
                )

            if not setting.ask_if_not_given:
                # print(
                #     f"Taking default `{setting.name}` value ({setting.default_value})."
                # )
                value = setting.default_value
            else:
                parameter_flag = False
                value_str = input(
                    f"Enter `{setting.name}` value ({values_to_print}), "
                    f"leave empty for default value ({setting.default_value}): "
                ).strip()

                if value_str == "":
                    print(
                        f"Nothing entered. Taking default `{setting.name}` value ({setting.default_value})."
                    )
                    value = setting.default_value
                elif setting.type is bool and value_str.lower() in {"0", "false", "f", "no", "n", "-"}:
                    print(
                        f"Entered value `{value_str}` for `{setting.name}` recognized as `False`."
                    )
                    value = 0
                elif setting.type is bool and value_str.lower() in {"1", "true", "t", "yes", "y", "+"}:
                    print(
                        f"Entered value `{value_str}` for `{setting.name}` recognized as `True`."
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
    def solver_index(self):
        """ Returns solver index """

        return self._solver_index

    @property
    def pre_build_patterns(self):
        """ Returns 'pre build all possible patterns list' setting """

        return self._pre_build_patterns

    @property
    def shuffle_before(self):
        """ Returns 'patterns shuffle before building list' setting """

        return self._shuffle_before

    @property
    def shuffle_after(self):
        """ Returns 'patterns shuffle after building list' setting """

        return self._shuffle_after

    @property
    def progress_timing(self):
        """ Returns `progress_timing` setting """

        return self._progress_timing

    @property
    def solver1_second_solution(self):
        """ Returns `solver1_second_solution` setting (only for Solver1) """

        return self._solver1_second_solution

    @property
    def solver2_random_pattern(self):
        """ Returns `solver2_random_pattern` setting (only for Solver2) """

        return self._solver2_random_pattern

    @property
    def all_colors_list(self):
        """ Returns `Colors` object containing list of pegs with all possible colors """

        return self._all_colors_list

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
