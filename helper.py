########################################
# My version of famous game Mastermind #
# helper.py                            #
# Mastermind Helper I/O file           #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import MastermindHelper


def main():
    """ Main I/O file for Mastermind Helper """

    mh = MastermindHelper(
        colors_number=8,
        pegs_number=8,
        turns_limit=0,
        shuffle_before=False,
        shuffle_after=False,
        solver_mode=2,
        progress_timing=True,
        mode1_second_solution=True,
        mode2_random_pattern=False,
    )

    mh.helper_intro()

    while not mh.game_status:
        try:
            mh.helper_take_turn(input(mh.helper_prompt))
        except ValueError as err:
            print(err)

    mh.helper_outro()


if __name__ == "__main__":
    main()
