########################################
# My version of famous game Mastermind #
# components.py                        #
# Mastermind components file           #
#             Piotr Loos (c) 2019-2020 #
########################################

from consts import *
from tools import Progress, shuffle


class Peg(int):
    """ Class for one pattern peg """

    def __str__(self):
        """ Formats `peg` to be printed """

        return f"({chr(self + 97)})"


class Pegs(list):
    """ Class for list of pegs """

    def __init__(self, colors_number):
        """ Initializes `Pegs` class object """

        super().__init__([Peg(peg_value) for peg_value in range(colors_number)])

    def __str__(self):
        """ Formats `Pegs` list to be printed """

        return f"{{{','.join(peg.__str__() for peg in self)}}}"


class Pattern(tuple):
    """ Class for one `pattern` """

    def __str__(self):
        """ Formats `pattern` to be printed """

        return f"[{''.join(peg.__str__() for peg in self)}]"


class Patterns(list):
    """ Class for list of all possible patterns (to be iterated on or to be filtered) """

    def __init__(self, settings):
        """ Generates all possible patterns """

        self._settings = settings

        patterns_list = [()]  # initialize temporary list containing empty tuple
        pegs_list = self._settings.pegs_list[:]  # get local `pegs_list` to be shuffled

        progress = Progress(
            items_number=sum(self._settings.colors_number ** i for i in range(1, self._settings.pegs_number + 1)),
            title="Building patterns list...",
            timing=self._settings.progress_timing,
        )

        progress.start()

        # iterate for `pegs_number`-1 times
        for _ in range(self._settings.pegs_number - 1):

            # shuffle `pegs_list` to build patterns from (on every iteration)
            if self._settings.shuffle_before:
                shuffle(
                    pegs_list,
                    progress=None,
                )

            # make temporary list of tuples (on every iteration)
            patterns_list = [
                progress.item((*pattern, new_peg))
                for pattern in patterns_list
                for new_peg in pegs_list
            ]
            # new pattern is tuple a one peg bigger (unpacked "old" pegs + "new" one)

        # shuffle `pegs_list` to build Pattern objects from
        if self._settings.shuffle_before:
            shuffle(
                pegs_list,
                progress=None,
            )

        # make final list of Pattern objects
        super().__init__(
            [
                progress.item(Pattern((*pattern, new_peg)))
                for pattern in patterns_list
                for new_peg in pegs_list
            ]
        )
        # new pattern is Pattern object a one peg bigger (unpacked "old" pegs + "new" one)

        progress.stop()

        # shuffle generated patterns list (whole list at once)
        if self._settings.shuffle_after:
            shuffle(
                self,
                progress=Progress(
                    items_number=self.__len__() - 1,
                    title="Shuffling patterns list...",
                    timing=self._settings.progress_timing,
                )
            )

    def print_patterns(self):
        """ Prints all patterns """

        for pattern in self:
            print(pattern)


class Response(tuple):
    """ Class for one response """

    def __str__(self):
        """ Formats `response` to be printed """

        return (
            "[{blacks}{whites}{dots}] ({black_number}, {white_number})"
            .format(
                blacks="●" * self[0],
                whites="○" * self[1],
                dots="∙" * (self[2] - self[0] - self[1]),
                black_number=self[0],
                white_number=self[1],
            )
        )

    @property
    def black_pegs(self):
        """ Returns `black_pegs` from `response` """

        return self[0]

    @property
    def white_pegs(self):
        """ Returns `white_pegs` from `response` """

        return self[1]


class Turn(tuple):
    """ Class for one game turn """

    def __str__(self):
        """ Formats `turn` to be printed """

        return (
            f"{self.turn_index:>3d}. {self.pattern} => {self.response}"
        )

    @property
    def turn_index(self):
        """ Returns `turn_index` from turn """

        return self[0]

    @property
    def pattern(self):
        """ Returns `pattern` from turn """

        return self[1]

    @property
    def response(self):
        """ Returns `response` from turn """

        return self[2]


class Turns(list):
    """ CLass for list of all turns in the game """

    def __init__(self):
        """ Initializes `Turns` class object """

        super().__init__()
        self._turns_index = 0

    def add_turn(self, pattern, response):
        """ Adds current turn to `Turns` """

        self._turns_index += 1
        self.append(Turn((self._turns_index, pattern, response)))

    def print_turns(self):
        """ Prints all turns """

        for turn in self:
            print(turn)

    @property
    def turns_index(self):
        """ Returns current turns index """

        return self._turns_index


class Settings:
    """ Class for all the game settings """

    def __init__(
            self,
            *args,
            colors_number=COLORS_NUMBER,
            pegs_number=PEGS_NUMBER,
            turns_limit=TURNS_LIMIT,
            solver_mode=SOLVER_MODE,
            shuffle_before=SHUFFLE_BEFORE,
            shuffle_after=SHUFFLE_AFTER,
            progress_timing=PROGRESS_TIMING,
            mode1_second_solution=MODE1_SECOND_SOLUTION,
            mode2_random_pattern=MODE2_RANDOM_PATTERN,
            **kwargs,
            ):
        """ Initializes `Settings` class object """

        # check if given number of colors is correct
        if colors_number in range(2, COLORS_NUMBER_MAX + 1):
            self._colors_number = colors_number
        else:
            raise ValueError(
                f"Incorrect number of colors ({colors_number})."
            )

        # check if given number of pegs is correct
        if pegs_number in range(2, PEGS_NUMBER_MAX + 1):
            self._pegs_number = pegs_number
        else:
            raise ValueError(
                f"Incorrect number of pegs ({pegs_number})."
            )

        # check if given `turns_limit` number is correct
        if turns_limit in range(0, TURNS_LIMIT_MAX + 1):  # turns_limit = 0 means unlimited turns
            self._turns_limit = turns_limit
        else:
            raise ValueError(
                f"Incorrect turns limit number ({turns_limit})."
            )

        # check if given `solver_mode` is correct
        if solver_mode in {1, 2}:
            self._solver_mode = solver_mode
        else:
            raise ValueError(
                f"Incorrect solving mode ({solver_mode})."
            )

        self._shuffle_before = bool(shuffle_before)
        self._shuffle_after = bool(shuffle_after)
        self._progress_timing = bool(progress_timing)
        self._mode1_second_solution = bool(mode1_second_solution)
        self._mode2_random_pattern = bool(mode2_random_pattern)

        self._pegs_list = Pegs(self._colors_number)

        for attribute in args:
            print(
                f"Attribute '{attribute}' has not been recognized! Ignoring."
            )

        for key, value in kwargs.items():
            print(
                f"Keyword '{key}' and it's value '{value}' has not been recognized! Ignoring."
            )

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
    def solver_mode(self):
        """ Returns solver mode number """

        return self._solver_mode

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
    def mode1_second_solution(self):
        """ Returns `second_solution` setting for Solver MODE 1 """

        return self._mode1_second_solution

    @property
    def mode2_random_pattern(self):
        """ Returns `random_pattern` setting for Solver MODE 2 """

        return self._mode2_random_pattern

    @property
    def pegs_list(self):
        """ Returns list of pegs """

        return self._pegs_list
