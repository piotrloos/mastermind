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

    class Peg(int):
        """ Class for one pattern peg """

        def __str__(self):
            """ Formats `peg` to be printed """

            # content = chr(self.__int__() + 97)
            content = self.__int__() + 1  # TODO: create setting for this

            if settings.colored_prints:

                # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

                colors_list = [
                    '31m',   # red
                    '93m',   # yellow
                    '32m',   # green
                    '34m',   # blue
                    '33m',   # orange
                    '35m',   # magenta
                    '90m',   # gray
                    '96m',   # cyan
                    '92m',   # bright green
                    '95m',   # bright magenta
                ]  # TODO: move it to settings
                return f"\033\133" \
                       f"{colors_list[self.__int__()]}" \
                       f"({content})" \
                       f"\033\13339m"
            else:
                return f"({content})"

        @classmethod
        def decode_peg(cls, peg_char):
            """ Returns Peg object converted from formatted `peg_char` """

            if len(peg_char) == 1:
                # return Peg(ord(peg_char) - 97)
                return Peg(int(peg_char) - 1)  # TODO: create setting for this

                # TODO: input digits, lowercase or uppercase letters, or own list of pegs
            else:
                return None

    Peg.all_colors_list = [Peg(color) for color in range(settings.colors_number)]

    return Peg


def pattern_class(settings):
    """ Function that creates and returns Pattern class with given `settings` """

    class Pattern(tuple):
        """ Class for one `pattern` """

        def __str__(self):
            """ Formats `pattern` to be printed """

            content = ''.join(peg.__str__() for peg in self)

            if settings.colored_prints:
                return f"\033\1331;51;38;5;255;255;255m{content}\033\133m"  # bold, framed, white fg
            else:
                return f"[{content}]"

        @classmethod
        def validate_pattern(cls, pattern_tuple):
            """ Checks if given `pattern_tuple` is formally correct """

            return (
                isinstance(pattern_tuple, tuple)
                and len(pattern_tuple) == settings.pegs_number
                and all(
                    pattern_peg in settings.Peg.all_colors_list
                    for pattern_peg in pattern_tuple
                )
            )

        @classmethod
        def decode_pattern(cls, pattern_string):
            """ Returns Pattern object converted from formatted `pattern_string` """

            try:
                pattern_tuple = tuple(
                    settings.Peg.decode_peg(peg_char)
                    for peg_char in pattern_string.replace(" ", "").replace(",", "")
                    # clean string and divide into pegs
                )
            except (TypeError, ValueError, IndexError):
                return None

            if cls.validate_pattern(pattern_tuple):
                return Pattern(pattern_tuple)
            else:
                return None

        @staticmethod
        def get_random_pattern():
            """ Returns random pattern for generating the solution or giving a demo pattern """

            return Pattern(
                settings.Peg.all_colors_list[randrange(settings.colors_number)]
                for _ in range(settings.pegs_number)
            )

        def calculate_black_pegs(self, other):
            """ Returns `black_pegs` number (how many pegs are in proper color and in proper location) """

            # return sum(
            #     int(self[index] == other[index])
            #     for index in range(settings.pegs_number)
            # )

            return sum(
                int(pattern1_peg == pattern2_peg)
                for pattern1_peg, pattern2_peg in zip(self, other)
            )

        def calculate_black_white_pegs(self, other):
            """ Returns `black_white_pegs` number (how many pegs are in proper color regardless to location) """

            # if not hasattr(self, '_color_dict'):
            #     self._color_dict = {color: self.count(color) for color in settings.all_colors_list}
            #     print(self._color_dict)

            return sum(
                min(self.count(color), other.count(color))
                for color in settings.Peg.all_colors_list
            )

        def calculate_response(self, other):
            """ Returns calculated Response object for given pattern related to other pattern """

            black_pegs = self.calculate_black_pegs(other)
            black_white_pegs = self.calculate_black_white_pegs(other)

            # `white_pegs` defines how many pegs are in proper color and wrong location
            # to calculate `white_pegs` it's needed to subtract `black_pegs` from `black_white_pegs`
            return settings.Response((black_pegs, black_white_pegs - black_pegs))

        @staticmethod
        def build_patterns():
            """ Returns list of all possible patterns (when `pre_build_patterns` setting == True) """

            if settings.use_itertools:

                with Progress(
                    items_number=settings.patterns_number,
                    color=settings.color,
                    title="[Pattern] Building patterns list (using itertools)...",
                    timing=settings.progress_timing,
                ) as progress:

                    # TODO: include `shuffle_colors_before_build` setting
                    all_patterns_list = list(map(lambda pattern_tuple: progress.item(settings.Pattern(pattern_tuple)),
                                                 product(settings.Peg.all_colors_list, repeat=settings.pegs_number)))
            else:

                with Progress(
                    items_number=sum(settings.colors_number ** i for i in range(1, settings.pegs_number + 1)),
                    color=settings.color,
                    title="[Pattern] Building patterns list (using my function)...",
                    timing=settings.progress_timing,
                ) as progress:

                    all_patterns_list = [()]  # initialize temporary list containing empty tuple
                    all_colors_list = settings.Peg.all_colors_list[:]  # get local `all_colors_list` to be shuffled

                    # TODO: let's shuffle colors once before build (new setting)

                    # iterate for `pegs_number`-1 times
                    for _ in range(settings.pegs_number - 1):

                        # shuffle `all_colors_list` to build patterns from (on every iteration)
                        if settings.shuffle_colors_before_build:
                            shuffle(
                                all_colors_list,
                            )

                        # make temporary list of tuples (on every iteration)
                        all_patterns_list = [
                            progress.item((*pattern, new_peg))
                            for pattern in all_patterns_list
                            for new_peg in all_colors_list
                        ]
                        # new pattern is tuple a one peg bigger (unpacked "old" pegs + "new" one)

                    # shuffle `all_colors_list` to build Pattern objects from
                    if settings.shuffle_colors_before_build:
                        shuffle(
                            all_colors_list,
                        )

                    # make final list of Pattern objects
                    all_patterns_list = [
                        progress.item(settings.Pattern((*pattern, new_peg)))
                        for pattern in all_patterns_list
                        for new_peg in all_colors_list
                    ]
                    # new pattern is Pattern object a one peg bigger (unpacked "old" pegs + "new" one)

            # shuffle generated patterns list (whole list at once)
            if settings.shuffle_patterns_after_build:
                with Progress(
                    items_number=len(all_patterns_list) - 1,
                    color=settings.color,
                    title="[Pattern] Shuffling patterns list...",
                    timing=settings.progress_timing,
                ) as progress:
                    shuffle(
                        all_patterns_list,
                        progress=progress,
                    )

            return all_patterns_list

        @staticmethod
        def gen_patterns():
            """ Generator for all possible patterns in the game (when `pre_build_patterns` setting == False) """

            all_colors_list = settings.Peg.all_colors_list
            colors_number = settings.colors_number
            pegs_number = settings.pegs_number

            if colors_number > 0:

                pattern = [all_colors_list[0]] * pegs_number  # get list of pegs with min values
                peg_index = pegs_number - 1  # set peg_index to last peg
                yield Pattern(pattern)

                if pegs_number > 0:

                    while True:  # infinite loop

                        peg = pattern[peg_index]  # get current peg from pattern
                        if peg < colors_number - 1:  # check if current peg has max value (=can be incremented?)

                            pattern[peg_index] = all_colors_list[peg + 1]  # increment current peg
                            peg_index = pegs_number - 1  # reset `peg_index` to last peg
                            yield Pattern(pattern)

                        else:  # current peg has max value -> need to carry one peg on the left

                            pattern[peg_index] = all_colors_list[0]  # reset current peg to min value
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

            return (
                "[{blacks}{whites}{dots}] ({black_number}, {white_number})"
                .format(
                    blacks="●" * self[0],
                    whites="○" * self[1],
                    dots="∙" * (settings.pegs_number - self[0] - self[1]),
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

        @property
        def black_white_pegs(self):
            """ Returns `black_pegs` + `white_pegs` from `response` """

            return self[0] + self[1]

        @classmethod
        def validate_response(cls, response_tuple):
            """ Checks if given `response_tuple` is formally correct """

            return (
                isinstance(response_tuple, tuple)
                and len(response_tuple) == 2
                and all(
                    response_peg in range(0, settings.pegs_number + 1)
                    for response_peg in {response_tuple[0], response_tuple[1], response_tuple[0] + response_tuple[1]}
                    # number of both black and white pegs (and sum of them also) should be between 0 and number of pegs
                )
            )

        @classmethod
        def decode_response(cls, response_string):
            """ Returns Response object converted from formatted `response_string` """

            try:
                response_tuple = tuple(
                    int(response_peg)
                    for response_peg in response_string.strip().split(' ', maxsplit=1)  # only one divide
                )
            except (TypeError, ValueError):
                return None

            if cls.validate_response(response_tuple):
                return Response(response_tuple)
            else:
                return None

        @classmethod
        def decode_pattern_response(cls, pattern_response_string):
            """ Returns Pattern and Response objects converted from formatted `pattern_response_string` """

            try:
                pattern, response = pattern_response_string.strip().split('=', maxsplit=1)  # only one divide at "="
            except (TypeError, ValueError):
                return None, None
            return settings.Pattern.decode_pattern(pattern), settings.Response.decode_response(response)

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
            """ Prints all turns """

            print(
                f"{f'There is 1 turn' if self._turns_index == 1 else f'There are {self._turns_index} turns'} "
                f"(so far) in this game:"
            )
            for turn in self:
                print(turn)

        @property
        def turns_index(self):
            """ Returns current turns index """

            return self._turns_index

    return TurnsList
