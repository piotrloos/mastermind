############################################
# My version of the famous Mastermind game #
# class_components.py                      #
# Mastermind components file               #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_tools import Progress, shuffle
from itertools import product
from random import randrange


def peg_class(settings):
    """ Function that creates and returns Peg class with given `settings` """

    # build list of peg chars
    peg_chars_list = ['.']  # first char '.' as blank peg

    if settings.use_digits_for_colors:
        peg_chars_list += list(
            [str(i) for i in range(1, 10)]  # char from '1' to '9'
            + ['0']  # char '0' as 10-th char
        )

    peg_chars_list += [chr(i) for i in range(ord('a'), ord('z') + 1)]  # chars from 'a' to 'z'
    peg_chars_list = peg_chars_list[:(settings.colors_number + 1)]  # save first `colors_number` elements (+ blank peg)

    class Peg(int):
        """ Class for one pattern peg """

        def __init__(self, peg_value):
            """ Checks if just created peg has valid value """

            # TODO: include `allow_blanks` setting
            if peg_value not in range(0, settings.colors_number + 1):  # with blank peg
                raise RuntimeError(
                    f"{settings.color.error_on}"
                    f"[Peg] Tried to create peg with invalid value!"
                    f"{settings.color.error_off}"
                )

        def __str__(self):
            """ Formats `peg` to be printed """

            peg_value = self.__int__()

            if settings.colored_prints:

                # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

                if peg_value == 0:
                    peg_color_code = '30'  # 0 black (blank peg)
                else:
                    # TODO: move color definitions to class_colors
                    peg_color_code_list = [
                        '95',   # 0 bright magenta
                        '31',   # 1 red
                        '93',   # 2 yellow
                        '32',   # 3 green
                        '34',   # 4 blue
                        '33',   # 5 orange
                        '35',   # 6 magenta
                        '90',   # 7 gray
                        '96',   # 8 cyan
                        '92',   # 9 bright green
                    ]
                    peg_color_code = peg_color_code_list[peg_value % 10]  # cyclic 10 colors above

                return (
                    f"\033\1331;{peg_color_code}m"  # bold on, color fg
                    f"({peg_chars_list[peg_value]})"
                    f"\033\13322;39m"  # bold off, reset fg
                )
            else:
                return (
                    f"({peg_chars_list[peg_value]})"
                )

        @classmethod
        def decode_peg(cls, peg_char):
            """ Returns Peg object converted from entered `peg_char` by the user """

            # TODO: include `allow_blanks` setting
            if len(peg_char) == 1:  # just one char
                try:
                    # find given char on the list
                    peg_value = peg_chars_list.index(peg_char.lower())  # accepted both lowercase and uppercase letters
                except IndexError:
                    raise ValueError

                return Peg.all_pegs_list[peg_value]  # with blank peg

            else:
                raise ValueError

    Peg.all_pegs_list = list(Peg(peg_value) for peg_value in range(0, settings.colors_number + 1))  # with blank peg

    return Peg


def pattern_class(settings):
    """ Function that creates and returns Pattern class with given `settings` """

    class Pattern(tuple):
        """ Class for one `pattern` """

        def __str__(self):
            """ Formats `pattern` to be printed """

            content = ''.join(peg.__str__() for peg in self)

            # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

            # TODO: move colors to class_colors
            if settings.colored_prints:
                return (
                    f"\033\13351m"  # enable framed pegs
                    f"{content}"
                    f"\033\13354m"  # disable framed pegs
                )
            else:
                return (
                    f"["
                    f"{content}"
                    f"]"
                )

        @classmethod
        def validate_pattern(cls, pattern_tuple):
            """ Checks if given `pattern_tuple` is formally correct """

            # TODO: include `allow_blanks` setting
            return (
                isinstance(pattern_tuple, tuple)
                and len(pattern_tuple) == settings.pegs_number
                and all(
                    pattern_peg in settings.Peg.all_pegs_list[1:]  # without blank peg
                    for pattern_peg in pattern_tuple
                )
            )

        @classmethod
        def decode_pattern(cls, user_pattern):
            """ Returns Pattern object converted from formatted `user_pattern` """

            try:
                # clean the string and divide into pegs
                pattern_tuple = tuple(
                    settings.Peg.decode_peg(peg_char)
                    for peg_char in user_pattern.replace(" ", "").replace(",", "")
                )
            except (TypeError, ValueError, IndexError):  # possible exceptions during decoding
                raise ValueError

            if cls.validate_pattern(pattern_tuple):
                return Pattern(pattern_tuple)
            else:
                raise ValueError

        @staticmethod
        def get_random_pattern():
            """ Returns random pattern for generating the solution or giving a demo pattern """

            # TODO: include `allow_blanks` setting
            return Pattern(
                tuple(
                    settings.Peg.all_pegs_list[randrange(1, settings.colors_number + 1)]  # without blank peg
                    for _ in range(settings.pegs_number)
                )
            )

        def calculate_black_pegs(self, other_pattern):
            """ Returns `black_pegs` number (how many pegs are in proper color and in proper location) """

            # TODO: include `allow_blanks` setting
            return sum(
                int(this_pattern_peg == other_pattern_peg)  # 0 (different pegs) or 1 (same peg)
                for this_pattern_peg, other_pattern_peg in zip(self, other_pattern)  # compare peg by peg
            )

        def calculate_black_white_pegs(self, other_pattern):
            """ Returns `black_white_pegs` number (how many pegs are in proper color regardless to location) """

            # TODO: include `allow_blanks` setting
            return sum(
                min(self.count(color), other_pattern.count(color))  # common number (minimum) of current color
                for color in settings.Peg.all_pegs_list[1:]  # without blank peg
            )

        def calculate_response(self, other_pattern):
            """ Returns calculated Response object for given pattern related to other pattern """

            black_pegs = self.calculate_black_pegs(other_pattern)
            black_white_pegs = self.calculate_black_white_pegs(other_pattern)

            # `white_pegs` defines how many pegs are in proper color and wrong location
            # to calculate `white_pegs` just subtract `black_pegs` from `black_white_pegs`
            return settings.Response((black_pegs, black_white_pegs - black_pegs))

        @staticmethod
        def build_patterns():
            """ Returns list of all possible patterns (when `pre_build_patterns` setting == True) """

            colors_list = settings.Peg.all_pegs_list[1:]  # get `colors_list` to be shuffled (copy) without blank peg

            # shuffle `colors_list` to build patterns from (before build)
            if settings.shuffle_colors_before_build:
                shuffle(
                    colors_list,  # small list
                    progress=None,  # without progress shown (quick operation)
                )

            # choose imported itertools.product function or my own function
            if settings.use_itertools:

                with Progress(
                    items_number=settings.patterns_number,
                    color=settings.color,
                    title="[Patterns] Building patterns list (using itertools)...",
                    timing=settings.progress_timing,
                ) as progress:

                    # TODO: use `shuffle_colors_during_build` setting (if possible)
                    all_patterns_list = list(
                        map(
                            # create Pattern objects using map function
                            lambda pattern_tuple: progress.item(settings.Pattern(pattern_tuple)),
                            product(colors_list, repeat=settings.pegs_number)
                        )
                    )
            else:

                with Progress(
                    # number of items is the sum of successive powers of `colors_number`
                    items_number=sum(settings.colors_number ** i for i in range(1, settings.pegs_number + 1)),
                    color=settings.color,
                    title="[Patterns] Building patterns list (using my own function)...",
                    timing=settings.progress_timing,
                ) as progress:

                    all_patterns_list = [()]  # initialize temporary list to be built (containing empty tuple)

                    # iterate for `pegs_number`-1 times
                    for _ in range(settings.pegs_number - 1):

                        # make temporary list of tuples
                        all_patterns_list = [
                            progress.item((*pattern, new_peg))
                            for pattern in all_patterns_list
                            for new_peg in colors_list
                        ]
                        # new pattern is tuple a one peg bigger (unpacked "old" pegs + "new" one)

                        # shuffle `colors_list` to build pattern from (during build)
                        if settings.shuffle_colors_during_build:
                            shuffle(
                                colors_list,  # small list
                                progress=None,  # without progress shown (quick operation)
                            )

                    # make final list of Pattern objects
                    all_patterns_list = [
                        progress.item(settings.Pattern((*pattern, new_peg)))  # create final Pattern objects
                        for pattern in all_patterns_list
                        for new_peg in colors_list
                    ]
                    # new pattern is Pattern object a one peg bigger (unpacked "old" pegs + "new" one)

            # shuffle generated patterns list (whole list at once) - regardless of the chosen method
            if settings.shuffle_patterns_after_build:
                with Progress(
                    items_number=len(all_patterns_list) - 1,
                    color=settings.color,
                    title="[Patterns] Shuffling patterns list...",
                    timing=settings.progress_timing,
                ) as progress:
                    shuffle(
                        all_patterns_list,  # big list
                        progress=progress,  # with progress shown (potentially slow operation)
                    )

            return all_patterns_list

        @staticmethod
        def gen_patterns():
            """ Generator for all possible patterns in the game (when `pre_build_patterns` setting == False) """

            colors_list = settings.Peg.all_pegs_list[1:]  # without blank peg
            # TODO: use `shuffle_colors_before_build` setting here

            colors_number = settings.colors_number
            pegs_number = settings.pegs_number

            if colors_number > 0:

                pattern_list = [colors_list[0]] * pegs_number  # get list of pegs with min values
                peg_index = pegs_number - 1  # set `peg_index` to last peg
                yield Pattern(tuple(pattern_list))  # yield the first patter

                # TODO: try to use `shuffle_colors_during_build` setting here

                if pegs_number > 0:

                    while True:  # infinite loop

                        # TODO: big jumps on the most significant pegs (without changing the least significant values)

                        peg = pattern_list[peg_index]  # get current peg from pattern_list
                        if peg < colors_number - 1:  # check if current peg has max value (=can be incremented?)

                            pattern_list[peg_index] = colors_list[peg + 1]  # increment current peg
                            peg_index = pegs_number - 1  # reset `peg_index` to last peg
                            yield Pattern(tuple(pattern_list))  # yield current pattern

                        else:  # current peg has max value -> need to carry one peg on the left

                            pattern_list[peg_index] = colors_list[0]  # reset current peg to min value
                            peg_index -= 1  # move `peg_index` to the left
                            if peg_index < 0:
                                break  # if `peg_index` reached first peg exit the loop

    return Pattern


def response_class(settings):
    """ Function that creates and returns Response class with given `settings` """

    class Response(tuple):
        """ Class for one response """

        def __str__(self):
            """ Formats `response` to be printed """

            # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

            return (
                f"{settings.color.response_on}" +
                "{blacks}{whites}{dots} ({black_number}, {white_number})"
                .format(
                    blacks="●" * self.black_pegs,
                    whites="○" * self.white_pegs,
                    dots="∙" * (settings.pegs_number - self.black_white_pegs),
                    black_number=self.black_pegs,
                    white_number=self.white_pegs,
                ) +
                f"{settings.color.response_off}"
            )

        @property
        def black_pegs(self):
            """ Returns `black_pegs` from `response` """

            return self[0]

        @property
        def white_pegs(self):
            """ Returns `white_pegs` from `response` """

            return self[1]

        @property
        def black_white_pegs(self):
            """ Returns `black_pegs` + `white_pegs` from `response` """

            return self[0] + self[1]

        @classmethod
        def validate_response(cls, response_tuple):
            """ Checks if given `response_tuple` is formally correct """

            return (
                isinstance(response_tuple, tuple)
                and len(response_tuple) == 2  # (black pegs number, white pegs number)
                and all(
                    response_peg in range(0, settings.pegs_number + 1)
                    for response_peg in {
                        response_tuple[0],  # black pegs number
                        response_tuple[1],  # white pegs number
                        response_tuple[0] + response_tuple[1],  # sum of black and white pegs
                    }
                    # all above numbers should be between 0 and `pegs_number`
                )
            )

        @classmethod
        def decode_response(cls, user_response):
            """ Returns Response object converted from `user_response` """

            try:
                # clean the string and divide to black_pegs and white_pegs
                response_tuple = tuple(
                    int(response_peg.strip())
                    for response_peg in user_response.strip().split(
                        sep=',',  # divide at comma
                        maxsplit=1,  # only one divide
                    )
                )
            except (TypeError, ValueError):  # possible exceptions during decoding
                raise ValueError

            if cls.validate_response(response_tuple):
                return Response(response_tuple)
            else:
                raise ValueError

        @classmethod
        def decode_pattern_response(cls, user_pattern_response):
            """ Returns Pattern and Response objects converted from `user_pattern_response` """

            try:
                user_pattern, user_response = user_pattern_response.strip().split(
                    sep='=',  # divide at equal sign
                    maxsplit=1,  # only one divide
                )
            except (TypeError, ValueError):  # possible exceptions during decoding
                raise ValueError

            if user_pattern.strip() == "":
                return (
                    None,
                    settings.Response.decode_response(user_response),
                )
            else:
                return (
                    settings.Pattern.decode_pattern(user_pattern),
                    settings.Response.decode_response(user_response),
                )

    return Response


def turn_class(settings):
    """ Function that creates and returns Turn class with given `settings` """

    if settings:
        pass  # TODO: use settings

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

    return Turn


def turns_list_class(settings):
    """ Function that creates and returns TurnsList class with given `settings` """

    class TurnsList(list):
        """ CLass for list of all turns in the game """

        def __init__(self):
            """ Initializes `TurnsList` class object """

            super().__init__()
            self._turns_index = 0

        def add_turn(self, pattern, response):
            """ Adds current turn to `TurnsList` """

            self._turns_index += 1
            turn = settings.Turn((self._turns_index, pattern, response))
            self.append(turn)
            return turn

        def print_turns_list(self):
            """ Prints all turns as a list """

            print(
                f"{f'There is 1 turn' if self._turns_index == 1 else f'There are {self._turns_index} turns'} "
                f"(so far) in this game:"
            )
            for turn in self:
                print(turn)
            print()

        @property
        def turns_index(self):
            """ Returns current turns index """

            return self._turns_index

    return TurnsList
