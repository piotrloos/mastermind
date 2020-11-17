########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main Mastermind base class file      #
#             Piotr Loos (c) 2019-2020 #
########################################

from abc import abstractmethod
from random import randrange
from components import Pattern, Response, Settings, Turns


class Mastermind:
    """ Contains whole game, base class for MastermindGame and MastermindSolver classes """

    @abstractmethod
    def __init__(
            self,
            *args,
            settings,
            **kwargs,
    ):
        """ Initializes new game with given settings """

        if isinstance(settings, Settings):
            self._settings = settings
        else:
            self._settings = Settings(*args, **kwargs)

        self._turns = Turns()  # initialize list of turns
        self._solution = None  # initialize solution field
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution

    @property
    def solution(self):
        """ Returns solution pattern (only when game is ended) """

        if self._game_status == 0:
            raise PermissionError(
                "No access to the solution when game is active!"
            )
        else:
            if self._solution is None:
                raise ValueError(
                    "No saved solution in this game!"
                )
            else:
                return self._solution

    def _get_random_pattern(self):
        """ Returns random pattern for generating the solution or giving a demo pattern """

        # TODO: random pattern from `all_patterns_list`?
        return Pattern(
            self._settings.all_colors_list[randrange(self._settings.colors_number)]
            for _ in range(self._settings.pegs_number)
        )

    def _decode_peg(self, peg_char):
        """ Returns Peg object converted from formatted `peg_char` """

        if len(peg_char) == 1:
            return self._settings.all_colors_list[ord(peg_char) - 97]
            # TODO: input digits, lowercase or uppercase letters, or own list of pegs
        else:
            return None

    def _decode_pattern(self, pattern_string):
        """ Returns Pattern object converted from formatted `pattern_string` """

        try:
            pattern_tuple = tuple(
                self._decode_peg(peg_char)
                for peg_char in pattern_string.replace(" ", "").replace(",", "")  # clean string and divide into pegs
            )
        except (TypeError, ValueError, IndexError):
            return None

        if self._validate_pattern(pattern_tuple):
            return Pattern(pattern_tuple)
        else:
            return None

    def _decode_response(self, response_string):
        """ Returns Response object converted from formatted `response_string` """

        try:
            response_tuple = tuple(
                int(response_peg)
                for response_peg in response_string.strip().split(' ', maxsplit=1)  # only one divide
            )
        except (TypeError, ValueError):
            return None

        if self._validate_response(response_tuple):
            return Response((*response_tuple, self._settings.pegs_number))  # black_pegs, white_pegs, pegs_number
        else:
            return None

    def _decode_pattern_response(self, pattern_response_string):
        """ Returns Pattern and Response objects converted from formatted `pattern_response_string` """

        try:
            pattern, response = pattern_response_string.strip().split('=', maxsplit=1)  # only one divide at "=" sign
        except (TypeError, ValueError):
            return None, None
        return self._decode_pattern(pattern), self._decode_response(response)

    # TODO: make it Pattern class method
    def _validate_pattern(self, pattern_tuple):
        """ Checks if given `pattern_tuple` is formally correct """

        return (
            isinstance(pattern_tuple, tuple)
            and len(pattern_tuple) == self._settings.pegs_number
            and all(
                pattern_peg in self._settings.all_colors_list
                for pattern_peg in pattern_tuple
            )
        )

    # TODO: make it Response class method
    def _validate_response(self, response_tuple):
        """ Checks if given `response_tuple` is formally correct """

        return (
            isinstance(response_tuple, tuple)
            and len(response_tuple) == 2
            and all(
                response_peg in range(0, self._settings.pegs_number + 1)
                for response_peg in {response_tuple[0], response_tuple[1], response_tuple[0] + response_tuple[1]}
                # number of both black and white pegs (and sum of them also) should be between 0 and number of pegs
            )
        )

    @staticmethod
    def _calculate_black_pegs(pattern1, pattern2):
        """ Returns `black_pegs` number (how many pegs are in proper color and in proper location) """

        return sum(
            int(pattern1_peg == pattern2_peg)
            for pattern1_peg, pattern2_peg in zip(pattern1, pattern2)
        )

    def _calculate_black_white_pegs(self, pattern1, pattern2):
        """ Returns `black_white_pegs` number (how many pegs are in proper color regardless to location) """

        return sum(
            min(pattern1.count(color_peg), pattern2.count(color_peg))
            for color_peg in self._settings.all_colors_list
        )

    def _calculate_response(self, pattern1, pattern2):
        """ Returns calculated Response object for given pattern related to other pattern """

        black_pegs = self._calculate_black_pegs(pattern1, pattern2)
        black_white_pegs = self._calculate_black_white_pegs(pattern1, pattern2)

        # `white_pegs` defines how many pegs are in proper color and wrong location
        # to calculate `white_pegs` it's needed to subtract `black_pegs` from `black_white_pegs`
        return Response((black_pegs, black_white_pegs - black_pegs, self._settings.pegs_number))
