############################################
# My version of the famous Mastermind game #
# main.py                                  #
# Mastermind main file                     #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

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

    if mode is None:
        raise RuntimeError(
            # f"{settings.color.error_on}"
            f"You did not specify Mastermind mode!\n"
            f"Try to run Mastermind with parameter mode=game, mode=helper or mode=solver."
            # f"{settings.color.error_off}"
        )
    elif mode == "game":
        MastermindGame(settings=Settings(**kwargs))
    elif mode == "helper":
        MastermindHelper(settings=Settings(**kwargs))
    elif mode == "solver":
        MastermindSolver(settings=Settings(**kwargs))
    else:
        raise RuntimeError(
            # f"{settings.color.error_on}"
            f"Given mode `{mode}` is incorrect!"
            # f"{settings.color.error_off}"
        )


if __name__ == "__main__":
    main()
