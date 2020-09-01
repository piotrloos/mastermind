########################################
# My version of famous game Mastermind #
# game.py                              #
# Mastermind Game I/O file             #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import MastermindGame


def main():
    """ Main I/O file for Mastermind Game """

    print()
    print("###################################")
    print("#   Welcome to Mastermind Game!   #")
    print("###################################")
    print()

    mg = MastermindGame(
        pegs_number=4,
        colors_number=6,
        turns_limit=12,
    )

    print(
        "I am the CodeMaker and I have prepared {pegs}-peg pattern using {colors} different colors: {list}."
        .format(
            pegs=mg.settings.pegs_number,
            colors=mg.settings.colors_number,
            list=mg.settings.pegs_list,
        )
    )
    print(
        "You are the CodeBreaker and you have {turns}"
        .format(
            turns=mg.settings.turns_limit,
        ),
        "turn" if mg.settings.turns_limit == 1 else "turns",
        "to guess the solution pattern."
    )
    print(
        "There are {number} possible patterns in this game. Example pattern is {pattern}."
        .format(
            number=mg.settings.patterns_number,
            pattern=mg.get_random_pattern(),
        )
    )
    print()

    while not mg.game_status:
        try:
            mg.game_take_turn(input(mg.game_prompt))
        except ValueError as err:
            print(err)
    print()

    if mg.game_status == 1:
        print(
            "You found the solution in {turns}"
            .format(
                turns=mg.turns_counter,
            ),
            "turn." if mg.turns_counter == 1 else "turns."
        )
    elif mg.game_status == 2:
        print("You reached turns limit. Game over!")

    print(
        "The solution was {pattern}."
        .format(
            pattern=mg.solution,
        )
    )

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
