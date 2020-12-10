########################################
# My version of famous game Mastermind #
# tools.py                             #
# Utility functions for Mastermind     #
#             Piotr Loos (c) 2019-2020 #
########################################

from random import randrange
from time import time


class Progress:
    """ Displays progress (percentage) during long-taking operations """

    def __init__(
            self,
            items_number,
            title="",
            timing=True,
            update_time_func=None,
    ):
        """ Initializes Progress class object """

        if items_number < 1:
            raise ValueError("The Progress process must last for one operation at least!")

        self._index = 0  # (int) index of current operation
        self._portion = items_number / 100  # (float) 1% of progress to be added to threshold
        self._inv = 100 / items_number  # (float) inversion of portion (to be * instead of /) to get the progress value
        self._threshold = self._portion  # (float) current threshold (start with 1%)
        self._threshold_int = int(round(self._threshold))  # (int) round the threshold to be compared with index

        self._title = str(title)  # (str) Progress process title to be displayed (if given)
        self._summary = ""  # (str) Progress process summary to be displayed (after finishing)

        self._timing = bool(timing)  # (bool) flag whether Progress process should be timed
        self._total_time = 0  # (float) total time in seconds
        self._start_time = None  # (float) last resume start timestamp

        self._update_time_func = update_time_func  # (func) func at host which allows to save (increment) progress time

        self._running = False  # (bool) flag whether Progress process is currently running
        self._finished = False  # (bool) flag whether Progress process is finished

    def __enter__(self):
        """ Initializes Progress context manager """

        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Ends Progress context manager """

        self.stop(finish=True)

    @staticmethod
    def _print(string):
        """ Outputs `string` in the same line """

        print(string, end="", flush=True)

    def _print_title_value(self):
        """ Prints `title` and `value` """

        self._print(
            f"\r{self._title} {int(round(self._index * self._inv)):3d}%"  # start from the beginning of line
        )

    def _print_value(self):
        """ Prints `value` """

        self._print(
            f"\b\b\b\b{int(round(self._index * self._inv)):3d}%"  # 4 backspaces and the new value (in the same place)
        )

    def _print_summary(self):
        """ Prints `summary` in place of `value` """

        self._print(
            f"\b\b\b\b{self._summary}\n"  # 4 backspaces and the summary (in the same place), go to the new line
        )

    def _check_state(self, should_be_running):
        """ Checks `finished` and `running` state and raises exception if needed """

        if self._finished:
            raise RuntimeError("Progress process is finished!")

        if should_be_running and not self._running:
            raise RuntimeError("Progress process is not running!")

        if not should_be_running and self._running:
            raise RuntimeError("Progress process is already running!")

    def start(self, title=None):
        """ Starts/resumes printing Progress process and changes `title` if given """

        if self._timing:
            self._start_time = time()

        self._check_state(should_be_running=False)
        self._running = True

        if title is not None:
            self._title = str(title)

        self._print_title_value()

    def stop(self, finish=True, summary="Done!"):
        """ Stops/pauses printing Progress process """

        self._check_state(should_be_running=True)
        self._running = False

        if finish:
            self._finished = True

        self._summary = summary

        if self._timing:
            partial_time = time() - self._start_time
            self._total_time += partial_time

            # TODO: 3 different states, clean it up
            self._summary += (
                f" (partial time: {partial_time:.3f}s{'' if not finish else f', total time: {self._total_time:.3f}s'})"
            )

            if self._update_time_func is not None:
                self._update_time_func(self._total_time)

        self._print_summary()

    def item(self, wrapped_value=None):
        """ Wraps value - checks if next Progress process value should be printed """

        self._index += 1

        if self._index >= self._threshold_int:

            self._check_state(should_be_running=True)

            self._print_value()  # calc the new Progress process value and print it
            self._threshold += self._portion  # (float) set the new threshold
            self._threshold_int = int(round(self._threshold))  # (int) round the threshold to be compared with index

        return wrapped_value


def shuffle(lst, progress=None):
    """ Shuffles iterable `lst` in place, handles Progress object if given """

    length = len(lst)

    for i in range(length - 1):
        j = randrange(i, length)
        lst[i], lst[j] = lst[j], lst[i]

        if progress is not None:
            progress.item()
