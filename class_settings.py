############################################
# My version of the famous Mastermind game #
# class_settings.py                        #
# Mastermind settings file                 #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_components import peg_class, pattern_class, response_class, guess_class, guesses_list_class
from class_consts import Consts
from class_styles import Color, NoColor
from class_solver1 import MastermindSolver1
from class_solver2 import MastermindSolver2
from itertools import product


class Settings:
    """ Class for all the game settings """

    def __init__(
            self,
            *args,

            styled_prints=None,
            use_digits_for_colors=None,
            progress_timing=None,
            print_guesses_list=None,

            peg_colors=None,
            pegs_in_pattern=None,
            allow_blanks=None,
            allow_duplicates=None,
            guesses_limit=None,

            chosen_solver=None,
            pre_build_patterns=None,
            use_itertools_for_build=None,
            shuffle_colors_before_build=None,
            shuffle_colors_during_build=None,
            shuffle_patterns_after_build=None,

            solver1_calc_2nd_solution=None,

            solver2_take_random_pattern=None,
            solver2_print_possible_solutions_threshold=None,

            **kwargs,
    ):
        """ Initializes `Settings` class object """

        # TERMINAL SETTINGS

        self._styled_prints = self._get_setting(
            Consts.StyledPrints,
            styled_prints,
        )
        self._use_digits_for_colors = self._get_setting(
            Consts.UseDigitsForColors,
            use_digits_for_colors,
        )
        self._progress_timing = self._get_setting(
            Consts.ProgressTiming,
            progress_timing,
        )
        self._print_guesses_list = self._get_setting(
            Consts.PrintGuessesList,
            print_guesses_list,
        )

        # MASTERMIND SETTINGS

        self._peg_colors = self._get_setting(
            Consts.PegColors,
            peg_colors,
        )
        self._pegs_in_pattern = self._get_setting(
            Consts.PegsInPattern,
            pegs_in_pattern,
        )
        self._allow_blanks = self._get_setting(
            Consts.AllowBlanks,
            allow_blanks,
        )
        self._allow_duplicates = self._get_setting(
            Consts.AllowDuplicates,
            allow_duplicates,
        )
        self._guesses_limit = self._get_setting(
            Consts.GuessesLimit,
            guesses_limit,
        )

        # SOLVING SETTINGS

        self._chosen_solver = self._get_setting(
            Consts.ChosenSolver,
            chosen_solver,
        )
        self._pre_build_patterns = self._get_setting(
            Consts.PreBuildPatterns,
            pre_build_patterns,
        )
        self._use_itertools_for_build = self._get_setting(
            Consts.UseItertoolsForBuild,
            use_itertools_for_build,
        )
        self._shuffle_colors_before_build = self._get_setting(
            Consts.ShuffleColorsBeforeBuild,
            shuffle_colors_before_build,
        )
        self._shuffle_colors_during_build = self._get_setting(
            Consts.ShuffleColorsDuringBuild,
            shuffle_colors_during_build,
        )
        self._shuffle_patterns_after_build = self._get_setting(
            Consts.ShufflePatternsAfterBuild,
            shuffle_patterns_after_build,
        )

        # SOLVER #1 SETTINGS

        self._solver1_calc_2nd_solution = self._get_setting(
            Consts.Solver1Calc2ndSolution,
            solver1_calc_2nd_solution,
        )

        # SOLVER #2 SETTINGS

        self._solver2_take_random_pattern = self._get_setting(
            Consts.Solver2TakeRandomPattern,
            solver2_take_random_pattern,
        )
        self._solver2_print_possible_solutions_threshold = self._get_setting(
            Consts.Solver2PrintPossibleSolutionsThreshold,
            solver2_print_possible_solutions_threshold,
        )

        if self._styled_prints:
            self.style = Color()
        else:
            self.style = NoColor()

        self._solvers_dict = {
            1: MastermindSolver1,  # patterns checking generator Solver
            2: MastermindSolver2,  # patterns list filtering Solver
        }

        for attribute in args:
            print(
                f"{self.style.error_on}"
                f"[Settings] Attribute "
                f"{self.style.attribute_on}"
                f"{attribute}"
                f"{self.style.attribute_off}"
                f" has not been recognized! Ignoring."
                f"{self.style.error_off}"
            )

        for key, value in kwargs.items():
            print(
                f"{self.style.error_on}"
                f"[Settings] Keyword "
                f"{self.style.attribute_on}"
                f"{key}"
                f"{self.style.attribute_off}"
                f" and it's value "
                f"{self.style.attribute_on}"
                f"{value}"
                f"{self.style.attribute_off}"
                f" has not been recognized! Ignoring."
                f"{self.style.error_off}"
            )

        # pin Classes to Settings instance
        self.Peg = peg_class(self)
        self.Pattern = pattern_class(self)
        self.Response = response_class(self)
        self.Guess = guess_class(self)
        self.GuessesList = guesses_list_class(self)

        self._all_patterns_list = None
        self._all_patterns_gen = None

        if self._pre_build_patterns:
            # build (and shuffle if enabled) all patterns list - once for several games
            self._all_patterns_list = self.Pattern.build_patterns()
        else:
            # TODO: try to use `shuffle_colors_before_build` and `shuffle_colors_during_build` settings (if possible)
            if self._use_itertools_for_build:
                self._all_patterns_gen = map(  # map generator
                    lambda pattern_tuple: self.Pattern(pattern_tuple),
                    product(  # get `itertools.product` generator
                        self.Peg.all_pegs_list[1:],  # without blank peg
                        repeat=self._pegs_in_pattern,  # repeat for every peg in pattern
                    )
                )
            else:
                # get reference for my generator (without call)
                self._all_patterns_gen = self.Pattern.gen_patterns

        print()

    @classmethod
    def _get_setting(cls, setting, value):
        """ Returns validated value (given as a parameter or entered by user) for setting and creates the property """

        if setting.type is bool:
            values_to_check = {0, False, 1, True}
            values_to_print = "0/False or 1/True"
        elif setting.type is int:
            values_to_check = range(setting.min_value, setting.max_value + 1)
            values_to_print = f"from {setting.min_value} to {setting.max_value}"
        else:
            raise TypeError(
                f"[Settings] Setting type `{setting.type}` for `{setting.name}` is incorrect!"
            )

        if setting.default_value not in values_to_check:
            raise RuntimeError(
                f"[Settings] Default `{setting.name}` value ({setting.default_value}) is incorrect!"
            )

        given_as_parameter = True  # flag to decide if the value is given as a parameter or entered by the user
        value_str = ""  # declare empty input value to ignore errors, although it will not be used before assignment

        while value not in values_to_check:

            if given_as_parameter:
                if value is not None:
                    print(
                        f"[Settings] Given `{setting.name}` value ({value}) as a parameter is incorrect!"
                    )
            else:
                print(
                    f"[Settings] Entered `{setting.name}` value ({value_str}) is incorrect!"
                )

            if not setting.ask_if_not_given:  # take default value
                print(
                    f"[Settings] Taking default `{setting.name}` value ({setting.default_value})."
                )
                value = setting.default_value
            else:  # ask the user
                given_as_parameter = False
                value_str = input(
                    f"[Settings] Enter `{setting.name}` ({setting.desc}) one value {values_to_print}, "
                    f"or leave empty for default value ({setting.default_value}): "
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
                    value = False
                elif setting.type is bool and value_str.lower() in {"1", "true", "t", "yes", "y", "v", "+"}:
                    print(
                        f"[Settings] Entered value `{value_str}` for `{setting.name}` recognized as `True`."
                    )
                    value = True
                else:
                    try:
                        value = int(value_str)  # try to treat value as int
                    except ValueError:
                        value = value_str  # if error occurred save as is

        # add new property with getter function returning setting value and disabled setter and deleter
        # for example let Settings.pegs_in_pattern return 4 value
        setattr(
            cls,  # this Settings class
            setting.name,  # used setting name for property
            property(
                fget=lambda _cls: value,  # getter function, omits first given argument `cls` and returns setting value
                fset=None,  # no setter function (read-only)
                fdel=None,  # no deleter function (read-only)
            )
        )

        return setting.type(value)  # returns value to be saved as a field in Settings object

    @property
    def patterns_number(self):
        """ Returns number of all possible patterns """

        # TODO: implement `allow_blanks` and `allow_duplicates` - patterns number will be different
        return self._peg_colors ** self._pegs_in_pattern  # `peg_colors` to the power of `pegs_in_pattern`

    @property
    def solver_class(self):
        """ Returns chosen Solver class (to be called) """

        return self._solvers_dict[self._chosen_solver]

    @property
    def all_colors_list_formatted(self):
        """ Returns formatted list of all possible colors """

        return (
            f"{{"  # one '{' char
            f"{','.join(peg.__str__() for peg in self.Peg.all_pegs_list[1:])}"  # without blank peg
            f"}}"  # one '}' char
        )

    @property
    def all_patterns_list(self):
        """ Returns reference to a list of all possible patterns """

        if self._all_patterns_list is None:
            raise RuntimeError(
                f"{self.style.error_on}"
                f"[Settings] List of all patterns is not generated yet!"
                f"{self.style.error_off}"
            )
        else:
            return self._all_patterns_list

    @property
    def all_patterns_gen(self):
        """ Returns reference to a generator of all possible patterns """

        if self._all_patterns_gen is None:
            raise RuntimeError(
                f"{self.style.error_on}"
                f"[Settings] Generator of all patterns is not defined yet!"
                f"{self.style.error_off}"
            )
        else:
            return self._all_patterns_gen
