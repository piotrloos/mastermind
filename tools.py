########################################
# My version of famous game Mastermind #
# tools.py                             #
# Utility functions for Mastermind     #
#             Piotr Loos (c) 2019-2020 #
########################################

from random import randrange


class Progress:
    """ Displays progress (percentage) during long-taking operations """

    def __init__(self, text, items_number):
        """ Initializes Progress class object """

        if items_number == 0:
            raise ValueError("The Progress must last for one operation at least!")

        self._index = 0
        self._inv = 100 / items_number
        self._portion = items_number / 100
        self._threshold = self._portion
        self._threshold_int = int(round(self._threshold))
        self._text = text or ""

    @staticmethod
    def _print(string):
        """ Outputs `string` in the same line """

        print(string, end="", flush=True)

    def _print_text_value(self, value):
        """ Prints `text` and `value` """

        self._print(
            "\r{text} {value:3d}%"
            .format(
                text=self._text,
                value=value,
            )
        )

    def _print_value(self, value):
        """ Prints `value` """

        self._print(
            "\b\b\b\b{value:3d}%"
            .format(
                value=value,
            )
        )

    def _print_end_text(self, text):
        """ Prints `text` in place of `value` """

        self._print(
            "\b\b\b\b{text}\n"
            .format(
                text=text,
            )
        )

    def start(self):
        """ Starts printing Progress """

        self._print_text_value(0)

    def item(self, outer_value=None):
        """ Wraps value - checks if next Progress value should be printed """

        self._index += 1
        if self._index >= self._threshold_int:
            self._print_value(int(round(self._index * self._inv)))
            self._threshold += self._portion
            self._threshold_int = int(round(self._threshold))
        return outer_value

    def rename(self, text):
        """ Changes Progress text """

        self._text = text or ""
        self._print_text_value(int(round(self._index * self._inv)))

    def stop(self, text="Done!"):
        """ Stops printing Progress """

        self._print_end_text(text)


def shuffle(lst, progress=None):
    """ Shuffles iterable `lst` in place, executes Progress object's method `item()` if given """

    length = len(lst)
    for i in range(length - 1):
        j = randrange(i, length)
        lst[i], lst[j] = lst[j], lst[i]
        if progress is not None:
            progress.item()
