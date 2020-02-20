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

    mg = MastermindGame(pegs=6, colors=8, turns_limit=20)

    print(
        "I am the CodeMaker and I have prepared {pegs}-peg pattern using {colors} different colors: {set}."
        .format(
            pegs=mg.pegs_number,
            colors=mg.colors_number,
            set=mg.colors_set,
        )
    )
    print(
        "You are the CodeBreaker and you have {turns}"
        .format(
            turns=mg.turns_limit,
        ),
        "turn" if mg.turns_limit == 1 else "turns",
        "to guess the solution pattern."
    )
    print(
        "There are {number} possible patterns in this game. Example pattern is {pattern}."
        .format(
            number=mg.patterns_number,
            pattern=mg.example_pattern,
        )
    )
    print()

    while not mg.game_status:
        try:
            print(mg.input(input(mg.prompt)))
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
