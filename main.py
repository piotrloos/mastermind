############################################
# My version of the famous Mastermind game #
# main.py                                  #
# Mastermind main file                     #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

import sys
from class_settings import Settings
from mode_game import MastermindGame
from mode_helper import MastermindHelper
from mode_solver import MastermindSolver


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
                pass  # do nothing if error occurred
            finally:
                kwargs[key] = value  # save the value (as int or str) to dict

    try:
        mode = kwargs["mode"].lower()  # try to get `mode` parameter
    except KeyError:
        mode = None  # no `mode` parameter specified
    else:
        del kwargs["mode"]  # if success delete from dict (not to be displayed furthermore)

    # TODO: try to use dict for Mastermind modes
    modes_to_check = {"1", "game", "2", "solver", "3", "helper"}
    modes_to_print = "1:Game, 2:Solver, 3:Helper"
    given_as_parameter = True  # flag to decide if the mode is given as a parameter or entered by the user
    mode_str = ""  # declare empty input value to ignore errors, although it will not be used before assignment

    while mode not in modes_to_check:

        if given_as_parameter:
            if mode is not None:
                print(
                    f"[Mastermind] Given `mode` value ({mode}) as a parameter is incorrect!"
                )
        else:
            print(
                f"[Mastermind] Entered `mode` value ({mode_str}) is incorrect!"
            )

        given_as_parameter = False
        mode_str = input(
            f"[Mastermind] Choose Mastermind mode: {modes_to_print}: "
        ).strip().lower()

        if mode_str in {"1", "game"}:
            mode = "game"
        elif mode_str in {"2", "solver"}:
            mode = "solver"
        elif mode_str in {"3", "helper"}:
            mode = "helper"
        else:
            mode = None

    settings = Settings(**kwargs)  # initialize Settings object and determine (set or ask for) missing settings

    # define sets of negative and positive user answers to play again question
    neg_answers_set = {"0", "false", "f", "no", "n", "x", "-", "exit"}
    pos_answers_set = {"1", "true", "t", "yes", "y", "v", "+", ""}
    all_answers_set = neg_answers_set.union(pos_answers_set)

    while True:
        if mode == "game":
            MastermindGame(settings=settings)
        elif mode == "helper":
            MastermindHelper(settings=settings)
        elif mode == "solver":
            MastermindSolver(settings=settings)
        else:
            raise RuntimeError(
                f"{settings.style.error_on}"
                f"[Mastermind] Given mode `{mode}` is incorrect!"
                f"{settings.style.error_off}"
            )

        # ask the user if he wants to play again
        again_str = None
        print()
        while again_str not in all_answers_set:
            again_str = input(
                "[Mastermind] Would you like do play again (y/n)? Leave empty for `yes`: "
            ).strip().lower()

        if again_str in neg_answers_set:
            break  # exit the game
        else:
            print()


if __name__ == "__main__":  # run only when it is called directly
    main()
