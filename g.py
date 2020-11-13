########################################
# My version of famous game Mastermind #
# game.py                              #
# Mastermind Game I/O file             #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import MastermindGame


def main():
    """ Main I/O file for Mastermind Game """

    MastermindGame(
        colors_number=6,
        pegs_number=4,
        turns_limit=12,
    )


if __name__ == "__main__":
    main()
