########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main Mastermind classes file         #
#             Piotr Loos (c) 2019-2020 #
########################################

from abc import abstractmethod
from random import randrange
from settings import *
from tools import Progress, shuffle


class PatternPeg:
    """ Class for one pattern peg """

    def __init__(self, peg):
        self._peg = peg

    def __str__(self):
        return (
            "({peg})"
            .format(
                peg=chr(self._peg + 97),  # TODO: implement different styles of formatting pattern
            )
        )

    def __repr__(self):
        return "Peg" + self.__str__()


class Pattern:
    """ Class for pattern """

    def __init__(self, pattern):
        self._pattern = tuple(pattern)

    def __str__(self):
        return (
            "[{pegs}]"
            .format(
                pegs="".join(peg.__str__() for peg in self._pattern),
            )
        )

    def __repr__(self):
        return "Pattern" + self.__str__()

    def __iter__(self):
        return self._pattern.__iter__()

    def count(self, peg):
        return self._pattern.count(peg)


class Response:
    """ Class for response """

    def __init__(self, black_pegs, white_pegs):
        self._black_pegs = black_pegs
        self._white_pegs = white_pegs

    def __str__(self):
        return (
            "[{blacks}{whites}{dots}] ({black_number}, {white_number})"
            .format(
                blacks="●" * self._black_pegs,
                whites="○" * self._white_pegs,
                dots="∙" * (10 - self._black_pegs - self._white_pegs),  # TODO: self._pegs_number
                black_number=self._black_pegs,
                white_number=self._white_pegs,
            )
        )

    def __eq__(self, response):
        return (
            self._black_pegs == response.black_pegs and self._white_pegs == response.white_pegs
        )

    @property
    def black_pegs(self):
        return self._black_pegs

    @property
    def white_pegs(self):
        return self._white_pegs


class Turn:
    """ Class for one game turn """

    def __init__(self, index, pattern, response):
        self._index = index
        self._pattern = pattern
        self._response = response

    def __str__(self):
        return (
            "{index:>{width}d}. {pattern} = {response}"
            .format(
                index=self._index,
                width=2,  # TODO: width  len(str(self._turns_limit))
                pattern=self._pattern,
                response=self._response,
            )
        )

    @property
    def index(self):
        return self._index

    @property
    def pattern(self):
        return self._pattern

    @property
    def response(self):
        return self._response


class TurnsContainer:
    def __init__(self):
        self._index = 0
        self._turns = []

    def __iter__(self):
        return self._turns.__iter__()

    def add_turn(self, pattern, response):
        self._index += 1
        self._turns.append(Turn(self._index, pattern, response))

    def print_turns(self):
        print()
        for turn in self._turns:
            print(turn)

    @property
    def index(self):
        return self._index


class PatternsContainer:
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def build(self):
        pass

    def print(self):
        pass

    def filter(self):
        pass


class SettingsContainer:
    def __init__(self,
                 *args,
                 colors=COLORS,
                 pegs=PEGS,
                 turns_limit=TURNS_LIMIT,
                 shuffle_before=SHUFFLE_BEFORE,
                 shuffle_after=SHUFFLE_AFTER,
                 solver_mode=SOLVER_MODE,
                 **kwargs,
                 ):

        # check if given `colors` number is correct
        if colors in range(2, MAX_COLORS + 1):
            self._colors = colors
        else:
            raise ValueError("Incorrect number of colors.")

        # check if given `pegs` number is correct
        if pegs in range(2, MAX_PEGS + 1):
            self._pegs = pegs
        else:
            raise ValueError("Incorrect number of pegs.")

        # check if given `turns_limit` number is correct
        if turns_limit in range(1, MAX_TURNS_LIMIT + 1):
            self._turns_limit = turns_limit
        else:
            raise ValueError("Incorrect number of turns limit.")

        # check if given `solver_mode` is correct
        if solver_mode in {1, 2}:
            self._solver_mode = solver_mode
        else:
            raise ValueError("Incorrect solving mode.")

        self._shuffle_before = bool(shuffle_before)
        self._shuffle_after = bool(shuffle_after)

        for attribute in args:
            print(
                "Attribute '{attribute}' hasn't been recognized! Ignoring."
                .format(
                    attribute=attribute,
                )
            )

        for key, value in kwargs.items():
            print(
                "Keyword '{key}' and it's value '{value}' hasn't been recognized! Ignoring."
                .format(
                    key=key,
                    value=value,
                )
            )

    @property
    def colors(self):
        """ Returns colors number """

        return self._colors

    @property
    def pegs(self):
        """ Returns pegs number """

        return self._pegs

    @property
    def patterns(self):
        """ Returns all possible patterns number """

        return self._colors ** self._pegs

    @property
    def turns_limit(self):
        """ Returns turns limit """

        return self._turns_limit

    @property
    def turns_width(self):
        """ Returns max width of turns integer """

        return len(str(self._turns_limit))

    @property
    def shuffle_before(self):
        """ Returns patterns shuffle before building list setting """

        return self._shuffle_before

    @property
    def shuffle_after(self):
        """ Returns patterns shuffle after building list setting """

        return self._shuffle_after

    @property
    def solver_mode(self):
        """ Returns solver mode number """

        return self._solver_mode


class Mastermind:
    """ Contains whole game, base class for MastermindGame and MastermindSolver classes """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """ Initializes new game with given settings """

        self._settings = SettingsContainer(*args, **kwargs)
        self._turns = TurnsContainer()  # initialize list of turns
        self._solution = None  # initialize solution field
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution
        self._colors_list = list(PatternPeg(value) for value in range(self._settings.colors))  # init pegs list

    @property
    def settings(self):
        return self._settings

    @property
    def turns(self):  # TODO: iteration through property?
        """ Returns turns list """

        return self._turns

    @property
    def turns_counter(self):
        """ Returns turn counter """

        return self._turns.index

    @property
    def solution(self):
        """ Returns formatted solution pattern only when game is ended """

        if self._game_status == 0:
            raise PermissionError("No access to the solution when game is active!")
        else:
            if self._solution is None:
                raise ValueError("No saved solution in this game!")
            else:
                return self._solution

    @property
    def game_status(self):
        """ Returns game status """

        return self._game_status

    @property
    def colors_list(self):
        """ Returns formatted set of colors """

        return (
            "{{{set}}}"
            .format(
                set=", ".join(peg.__str__() for peg in self._colors_list),  # TODO: __str__
            )
        )

    def get_random_pattern(self):
        """ Returns random pattern for generating the solution or giving a demo pattern """

        return Pattern(
            self._colors_list[randrange(self._settings.colors)]
            for _ in range(self._settings.pegs)
        )

    def _decode_peg(self, peg_char):
        """ Returns PatternPeg object converted from formatted `peg_char` """

        if len(peg_char) == 1:
            return self._colors_list[ord(peg_char) - 97]  # TODO: input digits, lowercase or uppercase letters
        else:
            return None

    def _decode_pattern(self, pattern_string):
        """ Returns Pattern object converted from formatted `pattern_string` """

        try:
            pattern_tuple = tuple(
                self._decode_peg(peg_char)
                for peg_char in pattern_string.replace(" ", "").replace(",", "")  # clean string and divide into pegs
            )
        except (TypeError, ValueError):
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
            return Response(*response_tuple)
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
            and len(pattern_tuple) == self._settings.pegs
            and all(
                pattern_peg in self._colors_list
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
                response_peg in range(0, self._settings.pegs + 1)
                for response_peg in {response_tuple[0], response_tuple[1], response_tuple[0] + response_tuple[1]}
                # both black and white pegs number (and sum of them also) should be between 0 and pegs number
            )
        )

    def calculate_response(self, pattern1, pattern2):
        """ Returns calculated Response object for given pattern related to other pattern """

        # `black_pegs` defines how many pegs are in proper color and in proper location
        black_pegs = sum(
            int(pattern1_peg == pattern2_peg)
            for pattern1_peg, pattern2_peg in zip(pattern1, pattern2)
        )

        # `black_white_pegs` defines how many pegs are in proper color regardless to location
        black_white_pegs = sum(
            min(pattern1.count(pattern_peg), pattern2.count(pattern_peg))
            for pattern_peg in self._colors_list
        )

        # `white_pegs` defines how many pegs are in proper color and wrong location
        # to calculate `white_pegs` it's needed to subtract `black_pegs` from `black_white_pegs`
        return Response(black_pegs, black_white_pegs - black_pegs)  # return response with black and white pegs

    def _check_game_end(self, response):
        """ Checks if the game should end (after current turn) """

        # check if all response pegs are black  # TODO: response from Mastermind object?
        if response.black_pegs == self._settings.pegs and response.white_pegs == 0:
            self._game_status = 1  # solution is found
            return True

        if self._turns.index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return True

        return False


class MastermindGame(Mastermind):
    """ Contains Mastermind Game mode, inherits from Mastermind class """

    def __init__(self,
                 *args,
                 solution=None,  # TODO: give tuple or Pattern object?
                 **kwargs,
                 ):
        """ Initializes Mastermind Game class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        if solution is None:  # check if `solution` is given
            self._solution = self.get_random_pattern()
        else:
            if self._validate_pattern(solution):  # TODO: validate Pattern object?
                self._solution = solution
            else:
                raise ValueError("Incorrect solution pattern.")

    @property
    def game_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{index:>{width}d}. Enter pattern: "
            .format(
                index=self._turns.index + 1,
                width=self._settings.turns_width,
            )
        )

    def game_take_turn(self, pattern_string, pattern=None):
        """ Takes turn as CodeMaker (with `pattern` or `pattern_string` from CodeBreaker) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if pattern is None:
            pattern = self._decode_pattern(pattern_string)
            if pattern is None:
                raise ValueError("Given pattern is incorrect! Enter again.")

        response = self.calculate_response(pattern, self._solution)  # TODO: save response to class object?

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()
        self._check_game_end(response)


class MastermindSolver(Mastermind):
    """ Contains Mastermind Solver mode, inherits from Mastermind class """

    def __init__(self, *args, **kwargs):
        """ Initializes Mastermind Solver class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        # TODO: new flag needed: `self._first_turn`

        # check if given `solver_mode` is correct
        if self.settings.solver_mode == 1:  # patterns checking generator mode
            self._solver = MastermindSolverMode1(self)  # TODO: giving (self) is OK?
        elif self.settings.solver_mode == 2:  # patterns list filtering mode
            self._solver = MastermindSolverMode2(self)  # TODO: giving (self) is OK?
        else:
            self._solver = None

    @property
    def poss_number(self):
        """ Returns possible solutions number """

        return self._solver.poss_number

    def get_patterns_list(self):
        """ Returns list of all pattern combinations using game settings """

        # generates all possible Pattern objects using my own function
        # it's similar to Cartesian product (`import itertools.product`),
        # but operates on tuples (Patterns at the last iteration) and works directly on Mastermind game settings

        all_patterns = [()]  # initialize with list containing empty tuple
        colors_list = self._colors_list[:]  # get local `colors_list` to be shuffled (if needed)

        progress = Progress(
            text="Building patterns list...",
            items_number=sum(self._settings.colors ** i for i in range(1, self._settings.pegs + 1)),  # sum of powers
        )

        progress.start()

        for _ in range(1, self._settings.pegs):  # iterate for pegs-1 times

            if self.settings.shuffle_before:  # shuffle `colors_list` to build patterns from (on every iteration)
                shuffle(
                    colors_list,
                    progress=None,
                )

            # make only temporary tuples instead of Pattern objects (for performance)
            all_patterns = [
                progress.item((*pattern, new_peg))
                for pattern in all_patterns
                for new_peg in colors_list
            ]
            # new pattern is tuple a one peg bigger (unpacked "old" pegs + "new" one)

        if self.settings.shuffle_before:  # shuffle `colors_list` to build patterns from
            shuffle(
                colors_list,
                progress=None,
            )

        # make Pattern objects at last iteration
        all_patterns = [
            progress.item(Pattern((*pattern, new_peg)))
            for pattern in all_patterns
            for new_peg in colors_list
        ]

        progress.stop()

        if self.settings.shuffle_after:  # shuffle `all_patterns` (whole list at once)
            shuffle(
                all_patterns,
                progress=Progress(
                    text="Shuffling patterns list...",
                    items_number=len(all_patterns) - 1,
                )
            )

        return all_patterns

    @property
    def solver_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{index:>{width}d}. Enter response for pattern {pattern}: "
            .format(
                index=self._turns.index + 1,
                width=self._settings.turns_width,
                pattern=self._solver.current_poss,
            )
        )

    def solver_take_turn(self, response_string, response=None):
        """ Takes turn as CodeBreaker (with `response` or `response_string` from CodeMaker) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if response is None:
            response = self._decode_response(response_string)
            if response is None:
                raise ValueError("Given response is incorrect! Enter again.")

        current_poss = self._solver.current_poss

        self._turns.add_turn(current_poss, response)
        self._turns.print_turns()

        if self._check_game_end(response):
            if self._game_status == 1:  # if the solution is found
                self._solution = current_poss  # save current possible solution as proper solution
        else:
            next_poss = self._solver.calculate_poss(current_poss, response)
            if next_poss is None:
                self._game_status = 3  # no possible solution found

            if self._solver.single_poss and self.game_status == 0:
                print("Now I know there is only one possible solution!")


class MastermindHelper(MastermindSolver):
    """ Contains Mastermind Helper mode, inherits from MastermindSolver class """

    def __init__(self, *args, **kwargs):
        """ Initializes Mastermind Helper class object """

        super().__init__(*args, **kwargs)  # initialize MastermindSolver class object

    @property
    def helper_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{index:>{width}d}. Enter pattern and it's response: "
            .format(
                index=self._turns.index + 1,
                width=self._settings.turns_width,
            )
        )

    def helper_take_turn(self, pattern_response_string, pattern=None, response=None):
        """ Takes turn in Helper mode (with `pattern` and `response` from human) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if pattern is None or response is None:
            pattern, response = self._decode_pattern_response(pattern_response_string)
            if pattern is None:
                raise ValueError("Given pattern is incorrect! Enter again.")
            if response is None:
                raise ValueError("Given response is incorrect! Enter again.")

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()

        if self._check_game_end(response):
            if self._game_status == 1:  # if the solution is found
                self._solution = pattern  # save current pattern as proper solution
        else:
            next_poss = self._solver.calculate_poss(pattern, response)
            if next_poss is None:
                self._game_status = 3  # no possible solution found
            else:
                print(
                    "One of the possible solution is: {pattern}"
                    .format(
                        pattern=next_poss,
                    )
                )

            if self._solver.single_poss and self.game_status == 0:
                print("Now I know there is only one possible solution!")


class MastermindSolverMode1:
    """ Contains Mastermind Solver MODE 1 (patterns checking generator mode) """

    def __init__(self, upper):
        """ (MODE 1) Initializes Mastermind Solver MODE 1 class object """

        self.super = upper  # TODO: is it OK?

        self._generator = MastermindSolverMode1Generator(self)  # initialize possible solutions generator
        self._current_poss = None  # initialize current possible solution
        self._second_poss = None  # initialize second possible solution
        self._single_poss = False  # initialize single possible solution flag

        self._get_next_poss()  # get first possible solution

    @property
    def current_poss(self):
        """ (MODE 1) Returns current possible solution (in this turn) """

        return self._current_poss

    @property
    def single_poss(self):
        """ (MODE 1) Returns single possible solution flag """

        return self._single_poss

    @property
    def poss_number(self):
        """ (MODE 1) Returns possible solutions number """

        raise NotImplementedError("It is impossible to calculate possible solutions number in MODE 1!")

    def check_poss(self, poss):
        """ (MODE 1) Checks if given possible solution still can be a solution based on all previous turns """

        return all(
            self.super.calculate_response(turn.pattern, poss) == turn.response
            for turn in self.super.turns
        )

    def calculate_poss(self, turn_pattern, turn_response):
        """ (MODE 1) Calculates the next possible solution after current turn """

        self._get_next_poss()  # get next possible solution
        return self._current_poss

    def _get_next_poss(self):
        """ (MODE 1) Saves next possible solution (if exists) """

        self._single_poss = False  # reset the flag

        # TODO: change `if` criteria (especially when `_second_poss` will be disabled)

        if self._current_poss is not None and self.check_poss(self._current_poss):
            print("Previously found first possible solution still can be a first solution. Not changed.")
        else:
            if self._second_poss is not None and self.check_poss(self._second_poss):
                print("Previously found second possible solution still can be a solution. Saved as first.")
                self._current_poss = self._second_poss
                self._second_poss = None
            else:
                try:
                    self._current_poss = self._generator.next("Searching for first possible solution...")
                except StopIteration:
                    self._current_poss = None  # no possible solution
                    self._second_poss = None  # no second possible solution also
                    return

        if self._second_poss is not None and self.check_poss(self._second_poss):
            print("Previously found second possible solution still can be a second solution. Not changed.")
        else:
            try:
                self._second_poss = self._generator.next("Searching for second possible solution...")
            except StopIteration:  # there is no second solution -> only one solution!
                self._single_poss = True  # set the flag
                self._second_poss = None  # no second possible solution


class MastermindSolverMode1Generator:
    """ (MODE 1) Contains possible solutions generator """

    def __init__(self, upper):
        """ (MODE 1 Generator) Initializes Mastermind Solver MODE 1 Generator class object """

        self.super = upper

        self._list = self.super.super.get_patterns_list()  # get list of all possible solutions to be checked
        self._index = 0  # initialize possible solutions index
        self._all = len(self._list)

        self._progress = Progress(
            text="",
            items_number=self._all,
        )

    def next(self, text=None):
        """ (MODE 1 Generator) Returns the first possible solution based on all previous turns """

        if text is not None:
            self._progress.rename(text)  # change the displayed text when needed

        while self._index < self._all:  # index between 0 and len()-1
            poss = self._list[self._index]  # get pattern from list
            self._index += 1  # now index is between 1 and len()

            if self._progress.item(self.super.check_poss(poss)):  # wrapped the long-taking operation
                self._progress.stop(
                    "Found! It's index is {index} of {all} overall ({percent:.2f}%)."
                    .format(
                        index=self._index,
                        all=self._all,
                        percent=100 * self._index / self._all,
                    )
                )
                return poss

        # after return the last pattern
        self._progress.stop(
            "Finished. Reached index {index} of {all} overall ({percent:.2f}%)."
            .format(
                index=self._index,
                all=self._all,
                percent=100 * self._index / self._all,  # should be always 100.00%
            )
        )
        raise StopIteration


class MastermindSolverMode2:
    """ Contains Mastermind Solver MODE 2 (patterns list filtering mode) """

    def __init__(self, upper):
        """ (MODE 2) Initializes Mastermind Solver MODE 2 class object """

        self.super = upper  # TODO: is it OK?

        self._poss_list = self.super.get_patterns_list()  # get list of all possible solutions to be filtered
        self._current_poss = None  # initialize current possible solution
        self._single_poss = False  # initialize single possible solution flag

        self._get_next_poss()  # get first possible solution

    @property
    def current_poss(self):
        """ (MODE 2) Returns current possible solution (in this turn) """

        return self._current_poss

    @property
    def single_poss(self):
        """ (MODE 2) Returns single possible solution flag """

        return self._single_poss

    @property
    def poss_number(self):
        """ (MODE 2) Returns possible solutions number """

        return len(self._poss_list)

    def calculate_poss(self, turn_pattern, turn_response):
        """ (MODE 2) Calculates the next possible solution after current turn """

        old_number = self.poss_number

        progress = Progress(
            text="Filtering patterns list...",
            items_number=old_number,
        )

        progress.start()

        # TODO: maybe remove items from list that don't meet condition?
        self._poss_list = [  # filter the existing list
            poss_pattern
            for poss_pattern in self._poss_list
            if progress.item(self.super.calculate_response(turn_pattern, poss_pattern) == turn_response)  # wrapped
        ]

        progress.stop()

        new_number = self.poss_number
        print(
            "Number of possible solutions is now {new} of {old} (rejected {percent:.2f}% of patterns)."
            .format(
                new=new_number,
                old=old_number,
                percent=100 * (1 - new_number / old_number),
            )
        )

        self._get_next_poss()  # get next possible solution
        return self._current_poss

    def _get_next_poss(self):
        """ (MODE 2) Saves next possible solution (if exists) """

        number = self.poss_number  # get the possible solutions number
        self._single_poss = (number == 1)  # set the flag if there is only one possible solution

        if number:  # check if there is at least one possible solution
            self._current_poss = self._poss_list[0]  # take first possible solution from the list
            # TODO: maybe random value? Not always 0? - parameter
        else:
            self._current_poss = None
