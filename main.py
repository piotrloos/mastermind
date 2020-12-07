########################################
# My version of famous game Mastermind #
# main.py                              #
# Mastermind main file                 #
#             Piotr Loos (c) 2019-2020 #
########################################

import sys
from settings import Settings
from game import MastermindGame
from helper import MastermindHelper
from solver import MastermindSolver


def main():
    """ Runs Mastermind game in given mode (Game, Helper, Solver) """

    kwargs = {}  # collected settings dict

    for kwarg in sys.argv:  # get parameters from command line arguments

        key = ""
        value = ""

        try:
            key, value, *_ = kwarg.split("=")  # try to divide at first "=" sign
        except ValueError:
            pass

        if key.strip() != "" and value.strip() != "":
            try:
                value = int(value)  # try to get integer arguments
            except (ValueError, TypeError):
                pass
            finally:
                kwargs[key] = value

    try:
        mode = kwargs["mode"].lower()  # try to get `mode` parameter
    except KeyError:
        mode = None
    else:
        del kwargs["mode"]  # if success delete from dict (not to be displayed furthermore)

    if mode == "game":
        MastermindGame(settings=Settings(**kwargs))
    elif mode == "helper":
        MastermindHelper(settings=Settings(**kwargs))
    elif mode == "solver":
        MastermindSolver(settings=Settings(**kwargs))
    else:
        if mode is None:
            raise RuntimeError(
                "You did not specify Mastermind mode!"
            )
        else:
            raise RuntimeError(
                f"Given mode `{mode}` is incorrect!"
            )


if __name__ == "__main__":
    main()
