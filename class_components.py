############################################
# My version of the famous Mastermind game #
# class_components.py                      #
# Mastermind main components file          #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_progress import Progress
from class_shuffle import shuffle
import itertools
from random import randrange


def peg_class(settings):
    """ Creates and returns Peg class with given `settings` """

    # build list of peg chars
    peg_chars_list = ['.']  # first char '.' as blank peg

    if settings.use_digits_for_colors:
        peg_chars_list += list(
            [str(i) for i in range(1, 10)]  # char from '1' to '9'
            + ['0']  # char '0' as 10-th char
        )

    peg_chars_list += [chr(i) for i in range(ord('a'), ord('z') + 1)]  # chars from 'a' to 'z'
    peg_chars_list = peg_chars_list[:(settings.peg_colors + 1)]  # save first `peg_colors` elements (+ blank peg)

    class Peg(int):
        """ Class for one pattern peg """

        def __init__(self, peg_color):
            """ Checks if just created peg has valid color """

            # TODO: include `allow_blanks` setting
            if peg_color not in range(0, settings.peg_colors + 1):  # with blank peg
                raise RuntimeError(
                    f"{settings.style.error_on}"
                    f"[Peg] Tried to create peg with invalid color!"
                    f"{settings.style.error_off}"
                )

        def __str__(self):
            """ Styles `peg` to be printed """

            peg_value = self.__int__()

            if settings.styled_prints:

                # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

                if peg_value == 0:
                    peg_color_code = '30'  # 0 black (blank peg)
                else:
                    # TODO: move color definitions to `class_styles`
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

        @property
        def char(self):
            """ Returns the char representing current Peg """

            return peg_chars_list[self.__int__()]

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

    Peg.all_pegs_list = list(Peg(peg_value) for peg_value in range(0, settings.peg_colors + 1))  # with blank peg

    return Peg


def pattern_class(settings):
    """ Creates and returns Pattern class with given `settings` """

    class Pattern(tuple):
        """ Class for one `pattern` """

        def __str__(self):
            """ Styles `pattern` to be printed """

            content = ''.join(peg.__str__() for peg in self)

            # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

            # TODO: move colors to `class_styles`
            if settings.styled_prints:
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
                and len(pattern_tuple) == settings.pegs_in_pattern
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
                    settings.Peg.all_pegs_list[randrange(1, settings.peg_colors + 1)]  # without blank peg
                    for _ in range(settings.pegs_in_pattern)
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
            """ Builds and returns a list of all possible patterns
            (when `pre_build_patterns` == True) """

            # copy `pegs_list` without blank peg to be saved (and shuffled if enabled)
            pegs_list = settings.Peg.all_pegs_list[1:]

            # shuffle `pegs_list` to build patterns from (before build) - if enabled
            if settings.shuffle_colors_before_build:
                shuffle(
                    pegs_list,  # small list
                    progress=None,  # without progress shown (quick operation)
                )

            if settings.use_itertools_for_build:  # choose imported itertools function

                with Progress(
                    items_number=settings.patterns_number,
                    style=settings.style,
                    title="[Pattern] Building patterns list (using itertools)...",
                    timing=settings.progress_timing,
                ) as progress:

                    # when using itertools it is impossible to use `shuffle_colors_during_build` setting

                    all_patterns_list = list(  # build the list from map generator
                        map(  # map function to create Pattern objects from tuples generated by itertools
                            lambda pattern_tuple: progress.item(  # wrapped to check the progress
                                settings.Pattern(pattern_tuple)
                            ),
                            itertools.product(  # returns Cartesian product of pegs_list repeated n times
                                pegs_list,
                                repeat=settings.pegs_in_pattern,  # repeat for length of the pattern
                            )
                        )
                    )

            else:  # choose my own function

                with Progress(
                    # number of items is the sum of successive powers of `peg_colors`
                    items_number=sum(settings.peg_colors ** i for i in range(1, settings.pegs_in_pattern + 1)),
                    style=settings.style,
                    title="[Pattern] Building patterns list (using my own function)...",
                    timing=settings.progress_timing,
                ) as progress:

                    all_patterns_list = [()]  # initialize temporary list to be built (containing empty pattern tuple)

                    for _ in range(settings.pegs_in_pattern - 1):  # iterate for `pegs_in_pattern`-1 times

                        all_patterns_list = [  # make temporary list of pattern tuples
                            progress.item(  # wrapped to check the progress
                                (*pattern_tuple, new_peg)  # unpack old tuple, add new peg and pack to new pattern tuple
                            )
                            for pattern_tuple in all_patterns_list
                            for new_peg in pegs_list
                        ]
                        # new pattern is tuple a one peg bigger (unpacked old pegs + new one)

                        # shuffle `pegs_list` to build pattern from (during build)
                        if settings.shuffle_colors_during_build:
                            shuffle(
                                pegs_list,  # small list
                                progress=None,  # without progress shown (quick operation)
                            )

                    all_patterns_list = [  # make final list of Pattern objects
                        progress.item(  # wrapped to check the progress
                            settings.Pattern(  # create final Pattern objects
                                (*pattern_tuple, new_peg)  # unpack old tuple, add new peg and pack to new pattern tuple
                            )
                        )
                        for pattern_tuple in all_patterns_list
                        for new_peg in pegs_list
                    ]
                    # new pattern is Pattern object a one peg bigger (unpacked old pegs + new one)

            # shuffle generated patterns list (whole list at once) - regardless of the chosen method
            if settings.shuffle_patterns_after_build:
                with Progress(
                    items_number=len(all_patterns_list) - 1,
                    style=settings.style,
                    title="[Pattern] Shuffling patterns list...",
                    timing=settings.progress_timing,
                ) as progress:
                    shuffle(
                        all_patterns_list,  # big list
                        progress=progress,  # with progress shown (potentially slow operation)
                    )

            return all_patterns_list

        @classmethod
        def patterns_generator(cls):
            """ Returns generator for all possible patterns in the game
            (when `pre_build_patterns` == False) """

            if settings.use_itertools_for_build:
                # assign the reference for itertools all patterns generator (without call)
                return cls._patterns_generator_itertools
            else:
                # assign the reference for my own all patterns generator (without call)
                return cls._patterns_generator_my_function

        @staticmethod
        def _patterns_generator_itertools():
            """ Returns generator for all possible patterns in the game using itertools function
            (when `pre_build_patterns` == False and `use_itertools_for_build` == True) """

            pegs_list = settings.Peg.all_pegs_list[1:]  # copy `pegs_list` without blank peg to be shuffled

            # shuffle `pegs_list` to build patterns from (before build)
            if settings.shuffle_colors_before_build:
                shuffle(
                    pegs_list,  # small list
                    progress=None,  # without progress shown (quick operation)
                )

            # when using itertools it is impossible to use `shuffle_colors_during_build` setting

            return map(  # map function to create Pattern objects from tuples generated by itertools
                lambda pattern_tuple: settings.Pattern(pattern_tuple),
                itertools.product(  # returns Cartesian product of pegs_list repeated n times
                    pegs_list,
                    repeat=settings.pegs_in_pattern,  # repeat for length of the pattern
                )
            )

            # when using patterns generator it is impossible to use `shuffle_patterns_after_build` setting

        @staticmethod
        def _patterns_generator_my_function():
            """ Returns generator for all possible patterns in the game using my own function
            (when `pre_build_patterns` == False and `use_itertools_for_build` == False) """

            # copy `pegs_list` without blank peg to be saved (and shuffled if enabled)
            pegs_list = settings.Peg.all_pegs_list[1:]

            # shuffle `pegs_list` to build patterns from (before build) - if enabled
            if settings.shuffle_colors_before_build:
                shuffle(
                    pegs_list,  # small list
                    progress=None,  # without progress shown (quick operation)
                )

            # create 2-dimensional matrix (dict values are lists) to keep `pegs_list` for every peg position in pattern
            pegs_lists_matrix = {}

            for peg_index in range(0, settings.pegs_in_pattern):  # `peg_index` from 0 to `pegs_in_pattern` - 1
                pegs_lists_matrix[peg_index] = pegs_list.copy()  # copy and save `pegs_list` for current `peg_index`

                # shuffle `pegs_list` for current peg (during build) - if enabled
                if settings.shuffle_colors_during_build:
                    shuffle(
                        pegs_lists_matrix[peg_index],  # small list
                        progress=None,  # without progress shown (quick operation)
                    )

            # to run faster the list like odometer with int values is used, instead of Pattern objects with Peg objects
            # conversion into mastermind objects and translation to shuffled value will occur during yielding a result
            # length of the odometer is `pegs_in_pattern` (indexed from 0), values are from 0 to `pegs_colors` - 1
            odometer = [0] * settings.pegs_in_pattern

            # yield the first pattern
            yield Pattern(  # create Pattern object
                tuple(  # from pattern tuple
                    map(  # where int values are converted into stored Peg objects from `pegs_list`
                        lambda odo_tuple: pegs_lists_matrix[odo_tuple[0]][odo_tuple[1]],  # matrix[index][value]
                        enumerate(odometer, 0),  # iterates and returns `odo_tuple` (index, value) from odometer
                    )
                )
            )

            # set `odo_index` to the least significant peg (initial position)
            odo_index = settings.pegs_in_pattern - 1

            while True:  # infinite loop

                # TODO: big jumps on the most significant pegs (without changing the least significant pegs)

                # check if current peg can be incremented (= peg has not max value yet)
                if odometer[odo_index] < settings.peg_colors - 1:

                    odometer[odo_index] += 1  # increment current peg
                    odo_index = settings.pegs_in_pattern - 1  # reset `odo_index` to the least significant peg

                    # yield current pattern after one increment
                    yield Pattern(  # create Pattern object
                        tuple(  # from pattern tuple
                            map(  # where int values are converted into stored Peg objects from `pegs_list`
                                lambda odo_tuple: pegs_lists_matrix[odo_tuple[0]][odo_tuple[1]],  # matrix[index][value]
                                enumerate(odometer, 0),  # iterates and returns `odo_tuple` (index, value) from odometer
                            )
                        )
                    )

                else:  # current peg has max value -> need to carry one peg on the left

                    odometer[odo_index] = 0  # reset current peg to min value
                    odo_index -= 1  # move `odo_index` to the left
                    if odo_index < 0:
                        # if `peg_index` reached the most significant peg (= all pegs have max value) finish generation
                        break

            # when using patterns generator it is impossible to use `shuffle_patterns_after_build` setting

    return Pattern


def response_class(settings):
    """ Creates and returns Response class with given `settings` """

    class Response(tuple):
        """ Class for one response """

        def __str__(self):
            """ Styles `response` to be printed """

            # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

            return (
                f"{settings.style.response_on}" +
                "{blacks}{whites}{dots} ({black_number}, {white_number})"
                .format(
                    blacks="●" * self.black_pegs,
                    whites="○" * self.white_pegs,
                    dots="∙" * (settings.pegs_in_pattern - self.black_white_pegs),
                    black_number=self.black_pegs,
                    white_number=self.white_pegs,
                ) +
                f"{settings.style.response_off}"
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
                    response_peg in range(0, settings.pegs_in_pattern + 1)
                    for response_peg in {
                        response_tuple[0],  # black pegs number
                        response_tuple[1],  # white pegs number
                        response_tuple[0] + response_tuple[1],  # sum of black and white pegs
                    }
                    # all above numbers should be between 0 and `pegs_in_pattern`
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


def guess_class(settings):
    """ Creates and returns Guess class with given `settings` """

    if settings:
        pass  # TODO: use settings

    class Guess(tuple):
        """ Class for one game guess """

        def __str__(self):
            """ Formats `guess` to be printed """

            return (
                f"{self.guess_index:>3d}. {self.pattern} => {self.response}"
            )

        @property
        def guess_index(self):
            """ Returns `guess_index` from `guess` """

            return self[0]

        @property
        def pattern(self):
            """ Returns `pattern` from `guess` """

            return self[1]

        @property
        def response(self):
            """ Returns `response` from `guess` """

            return self[2]

    return Guess


def guesses_list_class(settings):
    """ Creates and returns GuessesList class with given `settings` """

    class GuessesList(list):
        """ CLass for list of all guesses in the game """

        def __init__(self):
            """ Initializes `GuessesList` class object """

            super().__init__()
            self._guess_index = 0

        def add_guess(self, pattern, response):
            """ Adds current `guess` to `GuessesList` """

            self._guess_index += 1
            guess = settings.Guess((self._guess_index, pattern, response))
            self.append(guess)
            return guess

        def print_guesses_list(self):
            """ Prints list of all guesses """

            print(
                f"{f'There is 1 guess' if self._guess_index == 1 else f'There are {self._guess_index} guesses'} "
                f"(so far) in this game:"
            )
            for guess in self:
                print(guess)
            print()

        @property
        def guess_index(self):
            """ Returns current guesses index """

            return self._guess_index

    return GuessesList
