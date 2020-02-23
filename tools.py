########################################
# My version of famous game Mastermind #
# tools.py                             #
# Utility functions for Mastermind     #
#             Piotr Loos (c) 2019-2020 #
########################################

from random import randrange


class Progress:
    """ Displays progress (percentage) during long-taking operations """

    def __init__(self, text, item_number):
        """ Initializes Progress class object and prints first text """

        self._index = 0
        self._inv = 100 / item_number
        self._portion = item_number / 100
        self._threshold = self._portion
        self._threshold_int = int(round(self._threshold))
        print(text + "   0%", end='', flush=True)

    def item(self, value=None):
        """ Wraps value - checks if next progress text should be printed and prints it if yes """

        self._index += 1
        if self._index >= self._threshold_int:
            print("\b\b\b\b{:3}%".format(round(self._index * self._inv)), end='', flush=True)
            self._threshold += self._portion
            self._threshold_int = int(round(self._threshold))
        return value

    @staticmethod
    def delete():  # TODO: create a destructor
        """ Ends printing progress """

        print()

    # def __del__(self):
    #     """ Deletes Progress class object """
    #
    #     return super().__del__()


def shuffle(lst, p_obj=None):
    """ Shuffles iterable `lst` in place, executes Progress object's method `item()` if given """

    length = len(lst)
    for i in range(length - 1):
        j = randrange(i, length)
        lst[i], lst[j] = lst[j], lst[i]
        if p_obj is not None:
            p_obj.item()
