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

        self._index = 0
        self._inv = 100 / items_number
        self._portion = items_number / 100
        self._threshold = self._portion
        self._threshold_int = int(round(self._threshold))
        self._text = text

    def start(self):
        """ Starts printing progress """

        print(
            "\r{text} {value:3d}%"
            .format(
                text=self._text,
                value=0,
            ),
            end='',
            flush=True,
        )

    def item(self, value=None):
        """ Wraps value - checks if next progress value should be printed and prints it if yes """

        self._index += 1
        if self._index >= self._threshold_int:
            print(
                "\b\b\b\b{value:3d}%"
                .format(
                    value=int(round(self._index * self._inv)),
                ),
                end='',
                flush=True,
            )
            self._threshold += self._portion
            self._threshold_int = int(round(self._threshold))
        return value

    def rename(self, text):
        """ Changes the progress text and prints it """

        self._text = text
        print(
            "\r{text} {value:3d}%"
            .format(
                text=self._text,
                value=int(round(self._index * self._inv)),
            ),
            end='',
            flush=True,
        )

    @staticmethod
    def stop(text="Done!"):
        """ Stops printing progress and prints `text` """

        print(
            "\b\b\b\b{text}"
            .format(
                text=text,
            )
        )


def shuffle(lst, progress=None):
    """ Shuffles iterable `lst` in place, executes Progress object's method `item()` if given """

    length = len(lst)
    for i in range(length - 1):
        j = randrange(i, length)
        lst[i], lst[j] = lst[j], lst[i]
        if progress is not None:
            progress.item()
