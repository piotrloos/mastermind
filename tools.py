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

    def __init__(self, text, items_number, timing=True):
        """ Initializes Progress class object """

        if items_number < 1:
            raise ValueError("The Progress must last for one operation at least!")

        self._index = 0  # (int) index of current operation
        self._portion = items_number / 100  # (float) 1% of progress to be added to threshold
        self._inv = 100 / items_number  # (float) inversion of portion (to be * instead of /) to get the progress value
        self._threshold = self._portion  # (float) current threshold (start with 1%)
        self._threshold_int = int(round(self._threshold))  # (int) round the threshold to be compared with index
        self._text = text or ""  # (str) progress text to be displayed (if given)

        self._timing = timing  # (bool) flag whether Progress should be timed
        self._time_start = None
        self._time_stop = None

    @staticmethod
    def _print(string):
        """ Outputs `string` in the same line """

        print(string, end="", flush=True)

    def _print_text_value(self, value):
        """ Prints `text` and `value` """

        self._print(
            "\r{text} {value:3d}%"  # start from the beginning of line
            .format(
                text=self._text,
                value=value,
            )
        )

    def _print_value(self, value):
        """ Prints `value` """

        self._print(
            "\b\b\b\b{value:3d}%"  # 4 backspaces and the new value (in the same place)
            .format(
                value=value,
            )
        )

    def _print_end_text(self, text):
        """ Prints `text` in place of `value` """

        self._print(
            "\b\b\b\b{text}\n"  # 4 backspaces and the text (in the same place), go to the new line
            .format(
                text=text,
            )
        )

    def start(self):
        """ Starts printing Progress """

        if self._timing:
            self._time_start = time()

        self._print_text_value(0)  # start with 0%

    def item(self, outer_value=None):
        """ Wraps value - checks if next Progress value should be printed """

        self._index += 1
        if self._index >= self._threshold_int:
            self._print_value(int(round(self._index * self._inv)))  # calc the new progress value and print it
            self._threshold += self._portion  # (float) set the new threshold
            self._threshold_int = int(round(self._threshold))  # (int) round the threshold to be compared with index
        return outer_value

    def rename(self, text):
        """ Changes Progress text """

        self._text = text or ""
        self._print_text_value(int(round(self._index * self._inv)))

    def stop(self, text="Done!"):
        """ Stops printing Progress """

        if self._timing:
            self._time_stop = time()
            text += " (took {seconds:.2f}s)".format(
                seconds=self._time_stop-self._time_start,
            )

        self._print_end_text(text)


def shuffle(lst, progress=None):
    """ Shuffles iterable `lst` in place, handles Progress object if given """

    if progress is not None:
        progress.start()

    length = len(lst)

    for i in range(length - 1):
        j = randrange(i, length)
        lst[i], lst[j] = lst[j], lst[i]

        if progress is not None:
            progress.item()

    if progress is not None:
        progress.stop()
