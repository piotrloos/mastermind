############################################
# My version of the famous Mastermind game #
# mode_solver.py                           #
# Mastermind Solver                        #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from class_mastermind import Mastermind


class MastermindSolver(Mastermind):
    """ Contains Mastermind Solver mode, inherits from Mastermind class """

    # TODO: refactor MastermindGame, MastermindHelper, MastermindSolver into one class

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        """ Initializes `MastermindSolver` class object """

        super().__init__(*args, **kwargs)  # initialize Mastermind class object

        self._mode = "solver"

        class SolverStrings:
            greeting = "Welcome to Mastermind Solver!"
            codemaker_be = "You are"
            codemaker_have = "you have"
            codemaker_adjective = "your"
            codebreaker_be = "I am"
            codebreaker = "I"
            codebreaker_helper = "I"
            codebreaker_verb = "guess"

        self._strings = SolverStrings

        self._intro()
        self._solver_loop()
        self._outro()

    def _solver_loop(self):
        """ Main `Solver` loop """

        while not self._game_status:
            try:
                self._solver_take_turn(input(self._solver_prompt))
            except ValueError as err:
                print(err)

    @property
    def _possible_solutions_number(self):
        """ Returns number of possible solutions """

        return self._solver.possible_solutions_number

    @property
    def _solving_time(self):
        """ Returns total solving time """

        return self._solver.solving_time

    @property
    def _solver_prompt(self):
        """ Returns styled prompt for `input` function """

        return (
            f"{self._settings.style.number_on}"
            f"{self._guesses_list.guess_index + 1:>3d}."  # formatted as minimum 3 chars (spaces before number)
            f"{self._settings.style.number_off}"
            f" Enter `response` for pattern {self._solver.current_possible_solution}: "
        )

    # TODO: refactor with `helper_take_turn`
    def _solver_take_turn(self, user_response_string, computer_response=None):
        """ Takes a turn as the CodeBreaker (with `user_response_string` or `computer_response` from CodeMaker) """

        if self._game_status != 0:
            raise PermissionError(
                f"{self._settings.style.error_on}"
                f"[Solver] Game is ended! You can't take a turn."
                f"{self._settings.style.error_off}"
            )

        if computer_response is not None:  # computer is playing

            if type(computer_response) is not self._settings.Response:
                raise RuntimeError(
                    f"{self._settings.style.error_on}"
                    f"[Solver] Given `computer_response` is not the Response class object!"
                    f"{self._settings.style.error_off}"
                )
            else:
                response = computer_response

        else:  # user is playing

            try:
                response = self._settings.Response.decode_response(user_response_string)
            except ValueError:
                raise ValueError(
                    f"{self._settings.style.error_on}"
                    f"[Solver] You gave me incorrect `response`! Try something like `1,0`. Enter again."
                    f"{self._settings.style.error_off}"
                )

        pattern = self._solver.current_possible_solution
        print()

        guess = self._guesses_list.add_guess(pattern, response)

        if self._settings.print_guesses_list:
            self._guesses_list.print_guesses_list()

        # check game end criteria

        # check if all response pegs are black
        if response.black_pegs == self._settings.pegs_in_pattern and response.white_pegs == 0:
            self._solution = pattern  # save current pattern as proper solution
            self._game_status = 1  # solution is found
            return

        # check if the CodeBreaker reached guesses limit
        if self._settings.guesses_limit and self._guesses_list.guess_index >= self._settings.guesses_limit:
            self._game_status = 2  # reached guesses limit
            return

        # try to find the next possible solution
        # TODO: extract running calc function
        if self._solver.calculate_possible_solution(guess) is None:
            self._game_status = 3  # no possible solution found
            return

        # otherwise game is still active
