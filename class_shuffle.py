############################################
# My version of the famous Mastermind game #
# class_shuffle.py                         #
# Shuffle utility for Mastermind           #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from random import randrange


def shuffle(lst, progress=None):
    """ Shuffles iterable `lst` in place, handles Progress object if given """

    length = len(lst)

    for i in range(length - 1):
        j = randrange(i, length)
        lst[i], lst[j] = lst[j], lst[i]

        if progress is not None:
            progress.item()
