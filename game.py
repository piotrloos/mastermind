########################################
# My version of famous game Mastermind #
# game.py                              #
# Mastermind Game I/O file             #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import MastermindGame


def main():
    """ Main I/O file for Mastermind Game """

    mg = MastermindGame(
        colors_number=6,
        pegs_number=4,
        turns_limit=12,
    )

    mg.game_intro()

    while not mg.game_status:
        try:
            mg.game_take_turn(input(mg.game_prompt))
        except ValueError as err:
            print(err)

    mg.game_outro()


if __name__ == "__main__":
    main()
