########################################
# My version of famous game Mastermind #
# mastermind.py                        #
# Main Mastermind classes file         #
#             Piotr Loos (c) 2019-2020 #
########################################

from abc import abstractmethod
from random import randrange
from consts import *
from tools import Progress, shuffle


class Peg(int):
    """ Class for one pattern peg """

    def __str__(self):
        return (
            "({peg})"
            .format(
                peg=chr(super().__int__() + 97),  # TODO: implement different styles of formatting peg object
            )
        )


class PegsContainer(list):
    """ Class for list of pegs """

    def __init__(self, colors_number):
        super().__init__([Peg(peg_value) for peg_value in range(colors_number)])

    def __str__(self):
        return (
            "{{{pegs}}}"
            .format(
                pegs=",".join(peg.__str__() for peg in self),
            )
        )


class Pattern(tuple):
    """ Class for one pattern """

    def __str__(self):
        return (
            "[{pegs}]"
            .format(
                pegs="".join(peg.__str__() for peg in self),
            )
        )


class PatternsContainer(list):
    """ Class for list of all possible patterns (to be iterated on or to be filtered) """

    def __init__(self, settings):
        """ Generates all possible patterns """

        self._settings = settings

        patterns_list = [()]  # initialize temporary list containing empty tuple
        pegs_list = self._settings.pegs_list[:]  # get local `pegs_list` to be shuffled

        progress = Progress(
            text="Building patterns list...",
            items_number=sum(self._settings.colors_number ** i for i in range(1, self._settings.pegs_number + 1)),
            timing=True,
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
        super().__init__([
            progress.item(Pattern((*pattern, new_peg)))
            for pattern in patterns_list
            for new_peg in pegs_list
        ])
        # new pattern is Pattern object a one peg bigger (unpacked "old" pegs + "new" one)

        progress.stop()

        # shuffle generated patterns list (whole list at once)
        if self._settings.shuffle_after:
            shuffle(
                self,
                progress=Progress(
                    text="Shuffling patterns list...",
                    items_number=self.__len__() - 1,
                    timing=True,
                )
            )

    @property
    def patterns_number(self):
        return self.__len__()

    # TODO:
    def print(self):
        pass

    # TODO:
    def filter(self):
        pass


class Response(dict):  # TODO: namedtuple
    """ Class for one response """

    def __init__(self, black_pegs, white_pegs, pegs_number):
        super().__init__()
        self['black_pegs'] = black_pegs
        self['white_pegs'] = white_pegs
        self['pegs_number'] = pegs_number

    def __str__(self):
        return (
            "[{blacks}{whites}{dots}] ({black_number}, {white_number})"
            .format(
                blacks="●" * self['black_pegs'],
                whites="○" * self['white_pegs'],
                dots="∙" * (self['pegs_number'] - self['black_pegs'] - self['white_pegs']),
                black_number=self['black_pegs'],
                white_number=self['white_pegs'],
            )
        )

    @property
    def black_pegs(self):
        return self['black_pegs']

    @property
    def white_pegs(self):
        return self['white_pegs']


class Turn(dict):  # TODO: namedtuple
    """ Class for one game turn """

    def __init__(self, index, turns_width, pattern, response):
        super().__init__()
        self['index'] = index
        self['turns_width'] = turns_width
        self['pattern'] = pattern
        self['response'] = response

    def __str__(self):
        return (
            "{index:>{turns_width}d}. {pattern} = {response}"
            .format(
                index=self['index'],
                turns_width=self['turns_width'],
                pattern=self['pattern'],
                response=self['response'],
            )
        )

    @property
    def index(self):
        return self['index']

    @property
    def pattern(self):
        return self['pattern']

    @property
    def response(self):
        return self['response']


class TurnsContainer(list):
    def __init__(self, turns_width):
        super().__init__()
        self._turns_width = turns_width
        self._turns_index = 0

    def add_turn(self, pattern, response):
        self._turns_index += 1
        self.append(Turn(self._turns_index, self._turns_width, pattern, response))

    def print_turns(self):
        for turn in self:
            print(turn)

    @property
    def turns_index(self):
        return self._turns_index


class SettingsContainer:
    def __init__(self,
                 *args,
                 colors_number=COLORS_NUMBER,
                 pegs_number=PEGS_NUMBER,
                 turns_limit=TURNS_LIMIT,
                 shuffle_before=SHUFFLE_BEFORE,
                 shuffle_after=SHUFFLE_AFTER,
                 solver_mode=SOLVER_MODE,
                 **kwargs,
                 ):

        # check if given number of colors is correct
        if colors_number in range(2, COLORS_NUMBER_MAX + 1):
            self._colors_number = colors_number
        else:
            raise ValueError("Incorrect number of colors.")

        # check if given number of pegs is correct
        if pegs_number in range(2, PEGS_NUMBER_MAX + 1):
            self._pegs_number = pegs_number
        else:
            raise ValueError("Incorrect number of pegs.")

        # check if given `turns_limit` number is correct
        if turns_limit in range(1, TURNS_LIMIT_MAX + 1):
            self._turns_limit = turns_limit
        else:
            raise ValueError("Incorrect turns limit number.")

        # check if given `solver_mode` is correct
        if solver_mode in {1, 2}:
            self._solver_mode = solver_mode
        else:
            raise ValueError("Incorrect solving mode.")

        self._shuffle_before = bool(shuffle_before)
        self._shuffle_after = bool(shuffle_after)

        self._pegs_list = PegsContainer(self._colors_number)

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
    def turns_width(self):
        """ Returns max width of turns integer """

        return len(str(self._turns_limit))

    @property
    def shuffle_before(self):
        """ Returns 'patterns shuffle before building list' setting """

        return self._shuffle_before

    @property
    def shuffle_after(self):
        """ Returns 'patterns shuffle after building list' setting """

        return self._shuffle_after

    @property
    def solver_mode(self):
        """ Returns solver mode number """

        return self._solver_mode

    @property
    def pegs_list(self):
        """ Returns list of colors """

        return self._pegs_list


class Mastermind:
    """ Contains whole game, base class for MastermindGame and MastermindSolver classes """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """ Initializes new game with given settings """

        self._settings = SettingsContainer(*args, **kwargs)
        self._turns = TurnsContainer(self._settings.turns_width)  # initialize list of turns
        self._solution = None  # initialize solution field
        self._game_status = 0  # 0:game is active, 1:solution is found, 2:reached turns limit, 3:no possible solution

    @property
    def settings(self):
        """ Returns `SettingsContainer` class object """

        return self._settings

    @property
    def turns(self):  # TODO: iteration through property?
        """ Returns `TurnsContainer` class object """

        return self._turns

    @property
    def turns_counter(self):
        """ Returns turn counter """

        return self._turns.turns_index

    @property
    def solution(self):
        """ Returns solution pattern (only when game is ended) """

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

    def get_random_pattern(self):
        """ Returns random pattern for generating the solution or giving a demo pattern """

        return Pattern(
            self._settings.pegs_list[randrange(self._settings.colors_number)]
            for _ in range(self._settings.pegs_number)
        )

    def _decode_peg(self, peg_char):
        """ Returns Peg object converted from formatted `peg_char` """

        if len(peg_char) == 1:
            return self._settings.pegs_list[ord(peg_char) - 97]  # TODO: input digits, lowercase or uppercase letters
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
            return Response(*response_tuple, self._settings.pegs_number)
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
                pattern_peg in self._settings.pegs_list
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
            for pattern_peg in self._settings.pegs_list
        )

        # `white_pegs` defines how many pegs are in proper color and wrong location
        # to calculate `white_pegs` it's needed to subtract `black_pegs` from `black_white_pegs`
        return Response(black_pegs, black_white_pegs - black_pegs, self._settings.pegs_number)

    def _check_game_end(self, response):
        """ Checks if the game should end (after current turn) """

        # check if all response pegs are black  # TODO: response from Mastermind object?
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            self._game_status = 1  # solution is found
            return True

        if self._turns.turns_index >= self._settings.turns_limit:
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
                self._solution = Pattern(solution)
            else:
                raise ValueError("Incorrect solution pattern.")

    @property
    def game_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{index:>{width}d}. Enter pattern: "
            .format(
                index=self._turns.turns_index + 1,
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
        if self._settings.solver_mode == 1:  # patterns checking generator mode
            self._solver = MastermindSolverMode1(self._settings, self._turns, self.calculate_response)
        elif self._settings.solver_mode == 2:  # patterns list filtering mode
            self._solver = MastermindSolverMode2(self._settings, self._turns, self.calculate_response)
        else:
            self._solver = None

    @property
    def possible_solutions_number(self):
        """ Returns number of possible solutions """

        return self._solver.possible_solutions_number

    @property
    def solver_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{index:>{width}d}. Enter response for pattern {pattern}: "
            .format(
                index=self._turns.turns_index + 1,
                width=self._settings.turns_width,
                pattern=self._solver.current_possible_solution,
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

        current_poss = self._solver.current_possible_solution

        self._turns.add_turn(current_poss, response)
        self._turns.print_turns()

        if self._check_game_end(response):
            if self._game_status == 1:  # if the solution is found
                self._solution = current_poss  # save current possible solution as proper solution
        else:
            next_poss = self._solver.calculate_possible_solution(current_poss, response)
            if next_poss is None:
                self._game_status = 3  # no possible solution found

            if self._solver.single_solution_flag and self.game_status == 0:
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
                index=self._turns.turns_index + 1,
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
            next_poss = self._solver.calculate_possible_solution(pattern, response)
            if next_poss is None:
                self._game_status = 3  # no possible solution found
            else:
                print(
                    "One of the possible solution is: {pattern}"
                    .format(
                        pattern=next_poss,
                    )
                )

            if self._solver.single_solution_flag and self.game_status == 0:
                print("Now I know there is only one possible solution!")


class MastermindSolverMode1:
    """ Contains Mastermind Solver MODE 1 (patterns checking generator mode) """

    def __init__(self, settings, turns, calculate_response):
        """ (MODE 1) Initializes Mastermind Solver MODE 1 class object """

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns
        self._calculate_response = calculate_response

        # initialize possible solutions generator
        self._generator = MastermindSolverMode1Generator(self._settings, self._check_possible_solution)
        self._current_possible_solution = None
        self._second_possible_solution = None
        self._single_solution_flag = False

        self._get_next_poss()  # get first possible solution

    @property
    def current_possible_solution(self):
        """ (MODE 1) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def single_solution_flag(self):
        """ (MODE 1) Returns single possible solution flag """

        return self._single_solution_flag

    @property
    def possible_solutions_number(self):
        """ (MODE 1) Returns number of possible solutions """

        raise NotImplementedError("It is impossible to calculate number of possible solutions in MODE 1!")

    def _check_possible_solution(self, possible_solution):
        """ (MODE 1) Checks if given possible solution still can be a solution based on all previous turns """

        return all(
            self._calculate_response(turn.pattern, possible_solution) == turn.response
            for turn in self._turns
        )

    def calculate_possible_solution(self, turn_pattern, turn_response):
        """ (MODE 1) Calculates the next possible solution after current turn """

        self._get_next_poss()  # get next possible solution
        return self._current_possible_solution

    def _get_next_poss(self):
        """ (MODE 1) Saves next possible solution (if exists) """

        self._single_solution_flag = False  # reset the flag

        # TODO: change `if` criteria (especially when `_second_poss` will be disabled)

        if self._current_possible_solution is not None \
                and self._check_possible_solution(self._current_possible_solution):
            print("Previously found first possible solution still can be a first solution. Not changed.")
        else:
            if self._second_possible_solution is not None \
                    and self._check_possible_solution(self._second_possible_solution):
                print("Previously found second possible solution still can be a solution. Saved as first.")
                self._current_possible_solution = self._second_possible_solution
                self._second_possible_solution = None
            else:
                self._generator.rename("Searching for first possible solution...")
                try:
                    self._current_possible_solution = next(self._generator)
                except StopIteration:
                    self._current_possible_solution = None  # no possible solution
                    self._second_possible_solution = None  # no second possible solution also
                    return

        if self._second_possible_solution is not None and self._check_possible_solution(self._second_possible_solution):
            print("Previously found second possible solution still can be a second solution. Not changed.")
        else:
            self._generator.rename("Searching for second possible solution...")
            try:
                self._second_possible_solution = next(self._generator)
            except StopIteration:  # there is no second solution -> only one solution!
                self._single_solution_flag = True  # set the flag
                self._second_possible_solution = None  # no second possible solution


class MastermindSolverMode1Generator:
    """ (MODE 1) Contains possible solutions generator """

    def __init__(self, settings, check_possible_solution):
        """ (MODE 1 Generator) Initializes Mastermind Solver MODE 1 Generator class object """

        # TODO: temporary given labels
        self._settings = settings
        self._check_possible_solution = check_possible_solution

        self._patterns_list = PatternsContainer(self._settings)  # get list of all possible solutions to be checked
        self._patterns_index = 0  # initialize possible solutions index  # TODO: there is some bug with indexing
        self._patterns_number = self._patterns_list.patterns_number

        self._progress = Progress(
            text="",
            items_number=self._patterns_list.patterns_number,
            timing=False,
        )

    def rename(self, text):
        """ (MODE 1 Generator) Changes Progress object display text """
        self._progress.rename(text)

    def __iter__(self):  # TODO: is it necessary?
        return self

    def __next__(self):
        """ (MODE 1 Generator) Returns the first possible solution based on all previous turns """

        for pattern in self._patterns_list:

            self._patterns_index += 1  # index is between 1 and `self._patterns_number`

            if self._progress.item(self._check_possible_solution(pattern)):  # wrapped the long-taking operation
                self._progress.stop(
                    "Found! It's index is {index} of {all} overall ({percent:.2f}%)."
                    .format(
                        index=self._patterns_index,
                        all=self._patterns_number,
                        percent=100 * self._patterns_index / self._patterns_number,
                    )
                )
                return pattern

        # after return the last pattern
        self._progress.stop(
            "Finished. Reached index {index} of {all} overall ({percent:.2f}%)."
            .format(
                index=self._patterns_index,
                all=self._patterns_number,
                percent=100 * self._patterns_index / self._patterns_number,  # should be always 100.00%
            )
        )

        raise StopIteration


class MastermindSolverMode2:
    """ Contains Mastermind Solver MODE 2 (patterns list filtering mode) """

    def __init__(self, settings, turns, calculate_response):
        """ (MODE 2) Initializes Mastermind Solver MODE 2 class object """

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns
        self._calculate_response = calculate_response

        # TODO: filtering inside object (as method), not generated list from this object
        self._patterns_list = PatternsContainer(self._settings)  # get list of all possible solutions (to be filtered)
        # TODO: ^ for now it's PatternsContainer object, later it's just list
        self._patterns_number = self._patterns_list.patterns_number
        self._single_solution_flag = (self._patterns_number == 1)  # set the flag if there is only one possible solution

        if self._patterns_number:
            self._current_possible_solution = self._patterns_list[0]  # get first possible solution from the list
            # TODO: maybe random value? Not always 0? - parameter
        else:
            self._current_possible_solution = None

    @property
    def patterns_number(self):
        """ (MODE 2) Returns number of possible solutions """

        return self._patterns_number

    @property
    def current_possible_solution(self):
        """ (MODE 2) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def single_solution_flag(self):
        """ (MODE 2) Returns single possible solution flag """

        return self._single_solution_flag

    def calculate_possible_solution(self, turn_pattern, turn_response):
        """ (MODE 2) Calculates the next possible solution after current turn """

        old_patterns_number = self._patterns_number

        progress = Progress(
            text="Filtering patterns list...",
            items_number=old_patterns_number,
            timing=True,
        )

        progress.start()

        # filter the existing list
        # TODO: maybe remove items from list that don't meet condition?
        self._patterns_list = [
            possible_solution
            for possible_solution in self._patterns_list
            # TODO: ^ for first run it's PatternContainer object, then it's just list
            if progress.item(self._calculate_response(turn_pattern, possible_solution) == turn_response)
        ]

        progress.stop()

        self._patterns_number = len(self._patterns_list)
        self._single_solution_flag = (self._patterns_number == 1)

        if self._patterns_number:  # check if there is at least one possible solution
            self._current_possible_solution = self._patterns_list[0]  # get first possible solution from the list
            # TODO: maybe random value? Not always 0? - parameter
        else:
            self._current_possible_solution = None

        new_patterns_number = self._patterns_number
        print(
            "Number of possible solutions is now {new} of {old} (rejected {percent:.2f}% of patterns)."
            .format(
                new=new_patterns_number,
                old=old_patterns_number,
                percent=100 * (1 - new_patterns_number / old_patterns_number),
            )
        )

        return self._current_possible_solution
