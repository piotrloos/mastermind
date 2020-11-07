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
                peg=chr(self + 97),  # TODO: implement different styles of formatting peg object
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
                    items_number=self.__len__() - 1,
                    title="Shuffling patterns list...",
                    timing=self._settings.progress_timing,
                )
            )

    # TODO:
    def print(self):
        pass


class Response(tuple):
    """ Class for one response """

    def __str__(self):
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
        return self[0]

    @property
    def white_pegs(self):
        return self[1]


class Turn(tuple):
    """ Class for one game turn """

    def __str__(self):
        return (
            "{turn_index:>3d}. {pattern} => {response}"
            .format(
                turn_index=self[0],
                pattern=self[1],
                response=self[2],
            )
        )

    @property
    def pattern(self):
        return self[1]

    @property
    def response(self):
        return self[2]


class TurnsContainer(list):
    """ CLass for list of all turns in the game """

    def __init__(self):
        super().__init__()
        self._turns_index = 0

    def add_turn(self, pattern, response):
        self._turns_index += 1
        self.append(Turn((self._turns_index, pattern, response)))

    def print_turns(self):
        for turn in self:
            print(turn)

    @property
    def turns_index(self):
        return self._turns_index


class SettingsContainer:
    """ Class for all the game settings """

    def __init__(self,
                 *args,
                 colors_number=COLORS_NUMBER,
                 pegs_number=PEGS_NUMBER,
                 turns_limit=TURNS_LIMIT,
                 shuffle_before=SHUFFLE_BEFORE,
                 shuffle_after=SHUFFLE_AFTER,
                 solver_mode=SOLVER_MODE,
                 progress_timing=PROGRESS_TIMING,
                 mode1_second_solution=MODE1_SECOND_SOLUTION,
                 mode2_random_pattern=MODE2_RANDOM_PATTERN,
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
        if turns_limit in range(0, TURNS_LIMIT_MAX + 1):  # turns_limit = 0 means unlimited turns
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
        self._progress_timing = bool(progress_timing)
        self._mode1_second_solution = bool(mode1_second_solution)
        self._mode2_random_pattern = bool(mode2_random_pattern)

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


class Mastermind:
    """ Contains whole game, base class for MastermindGame and MastermindSolver classes """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """ Initializes new game with given settings """

        self._settings = SettingsContainer(*args, **kwargs)
        self._turns = TurnsContainer()  # initialize list of turns
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
            min(pattern1.count(pattern_peg), pattern2.count(pattern_peg))
            for pattern_peg in self._settings.pegs_list
        )

    def _calculate_response(self, pattern1, pattern2):
        """ Returns calculated Response object for given pattern related to other pattern """

        black_pegs = self._calculate_black_pegs(pattern1, pattern2)
        black_white_pegs = self._calculate_black_white_pegs(pattern1, pattern2)

        # `white_pegs` defines how many pegs are in proper color and wrong location
        # to calculate `white_pegs` it's needed to subtract `black_pegs` from `black_white_pegs`
        return Response((black_pegs, black_white_pegs - black_pegs, self._settings.pegs_number))


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
            "{index:>3d}. Enter `pattern`: "
            .format(
                index=self._turns.turns_index + 1,
            )
        )

    def game_take_turn(self, pattern_string, pattern=None):
        """ Takes turn as CodeMaker (with `pattern` or `pattern_string` from CodeBreaker) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if pattern is None:
            pattern = self._decode_pattern(pattern_string)
            if pattern is None:
                raise ValueError("Given `pattern` is incorrect! Enter again.")

        response = self._calculate_response(pattern, self._solution)

        # TODO: use Solver (MODE1) `check_possible_solution` method here
        #  to print info if given pattern could be the solution (like in Helper)

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            self._game_status = 1  # solution is found
            return

        if self._settings.turns_limit and self._turns.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return


class MastermindSolver(Mastermind):
    """ Contains Mastermind Solver mode, inherits from Mastermind class """

    def __init__(self, *args, **kwargs):
        """ Initializes Mastermind Solver class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        # TODO: new flag needed: `self._first_turn`

        solvers = {
            1: MastermindSolverMode1,  # patterns checking generator mode
            2: MastermindSolverMode2,  # patterns list filtering mode
        }

        self._solver = solvers[self._settings.solver_mode](
            self._settings,
            self._turns,
            self._calculate_black_pegs,
            self._calculate_black_white_pegs,
        )

    @property
    def possible_solutions_number(self):
        """ Returns number of possible solutions """

        return self._solver.possible_solutions_number

    @property
    def solver_prompt(self):
        """ Returns formatted prompt for `input` function """

        return (
            "{index:>3d}. Enter `response` for pattern {pattern}: "
            .format(
                index=self._turns.turns_index + 1,
                pattern=self._solver.current_possible_solution,
            )
        )

    # TODO: refactor with `helper_take_turn`
    def solver_take_turn(self, response_string, response=None):
        """ Takes turn as CodeBreaker (with `response` or `response_string` from CodeMaker) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if response is None:
            response = self._decode_response(response_string)
            if response is None:
                raise ValueError("Given `response` is incorrect! Enter again.")

        print()
        pattern = self._solver.current_possible_solution

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            self._solution = pattern  # save current pattern as proper solution
            self._game_status = 1  # solution is found
            return

        if self._settings.turns_limit and self._turns.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

        if self._solver.calculate_possible_solution(pattern, response) is None:
            self._game_status = 3  # no possible solution found
            return

        # game is still active

        if self._solver.single_solution_flag:
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
            "{index:>3d}. Enter `pattern=response` (empty pattern means {pattern}): "
            .format(
                index=self._turns.turns_index + 1,
                pattern=self._solver.current_possible_solution,
            )
        )

    # TODO: refactor with `solver_take_turn`
    def helper_take_turn(self, pattern_response_string, pattern=None, response=None):
        """ Takes turn in Helper mode (with `pattern` and `response` from human) """

        if self._game_status != 0:
            raise PermissionError("Game is ended! You can't take turn.")

        if pattern is None or response is None:
            pattern, response = self._decode_pattern_response(pattern_response_string)
            if pattern is None:
                pattern = self._solver.current_possible_solution  # get `pattern` if user enters "=response" only
            if response is None:
                raise ValueError("Given `pattern=response` is incorrect! Enter again.")

        print()
        if self._solver.check_possible_solution(pattern):
            print("Nice try. Given pattern could be the solution!")  # TODO: ...and sometimes "was the solution!"
        else:
            print("Unfortunately given pattern couldn't be the solution!")

        self._turns.add_turn(pattern, response)
        self._turns.print_turns()

        # check game end

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_number and response.white_pegs == 0:
            if self._solver.check_possible_solution(pattern):
                self._solution = pattern  # save current pattern as proper solution
                self._game_status = 1  # solution is found
            else:
                self._game_status = 3  # no possible solution found
            return

        if self._settings.turns_limit and self._turns.turns_index >= self._settings.turns_limit:
            self._game_status = 2  # reached turns limit
            return

        if self._solver.calculate_possible_solution(pattern, response) is None:
            self._game_status = 3  # no possible solution found
            return

        # game is still active

        print(
            "One of the possible solution is {pattern}."
            .format(
                pattern=self._solver.current_possible_solution,
            )
        )

        if self._solver.single_solution_flag:
            print("Now I know there is only one possible solution!")


class MastermindSolverMode1:
    """ Contains Mastermind Solver MODE 1 (patterns checking generator mode) """

    def __init__(self, settings, turns, calculate_black_pegs, calculate_black_white_pegs):
        """ (MODE 1) Initializes Mastermind Solver MODE 1 class object """

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns
        self._calculate_black_pegs = calculate_black_pegs
        self._calculate_black_white_pegs = calculate_black_white_pegs

        self._generator = MastermindSolverMode1Generator(self._settings, self.check_possible_solution)
        self._current_possible_solution = None
        self._second_possible_solution = None
        self._single_solution_flag = False

        self.calculate_possible_solution()  # get first possible solution

    @property
    def possible_solutions_number(self):
        """ (MODE 1) Returns number of possible solutions """

        raise NotImplementedError("It is impossible to calculate number of possible solutions in MODE 1!")

    @property
    def current_possible_solution(self):
        """ (MODE 1) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def single_solution_flag(self):
        """ (MODE 1) Returns single possible solution flag """

        return self._single_solution_flag

    def check_possible_solution(self, possible_solution):
        """ (MODE 1) Checks if given possible solution can be a solution based on all previous turns """

        if possible_solution is None:
            return False

        # TODO: try to speed up these calculations
        return all(
            self._calculate_black_pegs(turn.pattern, possible_solution) ==
            turn.response.black_pegs
            and
            self._calculate_black_white_pegs(turn.pattern, possible_solution) ==
            turn.response.black_pegs + turn.response.white_pegs
            for turn in self._turns
        )

    def calculate_possible_solution(self, *_):
        """ (MODE 1) Calculates the next possible solution after current turn """

        # TODO: refactor this method to avoid bug in Progress state (when generator is exhausted)

        self._single_solution_flag = False  # reset the flag

        if self.check_possible_solution(self._current_possible_solution):
            print("Previously found first possible solution still can be a first solution. Not changed.")
        else:
            if self._settings.mode1_second_solution and self.check_possible_solution(self._second_possible_solution):
                print("Previously found second possible solution still can be a solution. Saved as first.")
                self._current_possible_solution = self._second_possible_solution
                self._second_possible_solution = None
            else:
                try:
                    self._current_possible_solution = self._generator.next("Searching for first possible solution...")
                    # TODO: ^^ not always `first`
                except StopIteration:
                    self._current_possible_solution = None  # no possible solution
                    self._second_possible_solution = None  # no second possible solution also
                    return None

        if self._settings.mode1_second_solution:
            if self.check_possible_solution(self._second_possible_solution):
                print("Previously found second possible solution still can be a second solution. Not changed.")
            else:
                try:
                    self._second_possible_solution = self._generator.next("Searching for second possible solution...")
                except StopIteration:  # there is no second solution -> only one solution!
                    self._second_possible_solution = None  # no second possible solution
                    self._single_solution_flag = True  # set the flag

        return self._current_possible_solution


class MastermindSolverMode1Generator:
    """ (MODE 1) Contains possible solutions generator """

    def __init__(self, settings, check_possible_solution):
        """ (MODE 1 Generator) Initializes Mastermind Solver MODE 1 Generator class object """

        # TODO: temporary given labels
        self._settings = settings
        self._check_possible_solution = check_possible_solution

        self._patterns_list = PatternsContainer(self._settings)  # get list of all possible solutions to be checked
        self._patterns_index = 0  # initialize possible solutions index
        self._patterns_number = len(self._patterns_list)

        self._progress = Progress(
            items_number=self._patterns_number,
            title="",
            timing=self._settings.progress_timing,
        )

    def next(self, progress_title):
        """ (MODE 1 Generator) Returns the first possible solution based on all previous turns """

        self._progress.start(
            title=progress_title,
        )

        while self._patterns_index < self._patterns_number:  # index is between 0 and `patterns_number`-1

            pattern = self._patterns_list[self._patterns_index]  # get pattern from list
            self._patterns_index += 1  # index is now between 1 and `patterns_number`

            if self._progress.item(self._check_possible_solution(pattern)):  # wrapped the long-taking operation
                self._progress.stop(
                    pause=True,
                    summary="Found! It's index is {index} of {all} overall ({percent:.2f}%)."
                    .format(
                        index=self._patterns_index,
                        all=self._patterns_number,
                        percent=100 * self._patterns_index / self._patterns_number,
                    ),
                )
                return pattern

        # after return the last pattern
        self._progress.stop(
            pause=False,
            summary="Finished. Reached index {index} of {all} overall ({percent:.2f}%)."
            .format(
                index=self._patterns_index,
                all=self._patterns_number,
                percent=100 * self._patterns_index / self._patterns_number,  # should be always 100.00%
            ),
        )

        raise StopIteration


class MastermindSolverMode2:
    """ Contains Mastermind Solver MODE 2 (patterns list filtering mode) """

    def __init__(self, settings, turns, calculate_black_pegs, calculate_black_white_pegs):
        """ (MODE 2) Initializes Mastermind Solver MODE 2 class object """

        # TODO: temporary given labels
        self._settings = settings
        self._turns = turns
        self._calculate_black_pegs = calculate_black_pegs
        self._calculate_black_white_pegs = calculate_black_white_pegs

        # TODO: for first time it's PatternsContainer object, later it's just list
        self._possible_solutions_list = PatternsContainer(self._settings)  # get list of all possible solutions
        self._analyze_the_list()

    def _analyze_the_list(self):
        """ (MODE 2) Gets the possible solution, gets the possible solutions number and sets the flag """

        self._possible_solutions_number = len(self._possible_solutions_list)
        self._single_solution_flag = (self._possible_solutions_number == 1)

        if self._settings.mode2_random_pattern:
            index = randrange(self._possible_solutions_number)
        else:
            index = 0

        try:
            self._current_possible_solution = self._possible_solutions_list[index]
        except IndexError:
            self._current_possible_solution = None

    @property
    def possible_solutions_number(self):
        """ (MODE 2) Returns number of possible solutions """

        return self._possible_solutions_number

    @property
    def current_possible_solution(self):
        """ (MODE 2) Returns current possible solution (in this turn) """

        return self._current_possible_solution

    @property
    def single_solution_flag(self):
        """ (MODE 2) Returns single possible solution flag """

        return self._single_solution_flag

    def check_possible_solution(self, possible_solution):
        """ (MODE 2) Checks if given possible solution can be a solution based on all previous turns """

        return possible_solution in self._possible_solutions_list

    def calculate_possible_solution(self, turn_pattern, turn_response, *_):
        """ (MODE 2) Calculates the next possible solution after current turn """

        patterns_old_number = self._possible_solutions_number

        progress = Progress(
            items_number=patterns_old_number,
            title="Filtering patterns list...",
            timing=self._settings.progress_timing,
        )

        progress.start()

        # TODO: try to speed up these calculations
        self._possible_solutions_list = [
            possible_solution
            for possible_solution in self._possible_solutions_list
            if progress.item(
                self._calculate_black_pegs(turn_pattern, possible_solution) ==
                turn_response.black_pegs
                and
                self._calculate_black_white_pegs(turn_pattern, possible_solution) ==
                turn_response.black_pegs + turn_response.white_pegs
            )
        ]

        progress.stop()

        self._analyze_the_list()

        patterns_new_number = self._possible_solutions_number
        print(
            "Number of possible solutions is now {new} of {old} (rejected {percent:.2f}% of patterns)."
            .format(
                new=patterns_new_number,
                old=patterns_old_number,
                percent=100 * (1 - patterns_new_number / patterns_old_number),
            )
        )

        return self._current_possible_solution
