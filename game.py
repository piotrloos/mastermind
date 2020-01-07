########################################
# My version of famous game Mastermind #
# game.py                              #
# CodeMaker file                       #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import CodeMaker


def main():
    """ Main I/O file for Mastermind CodeMaker """

    print()
    print("##############################")
    print("#   Welcome to Mastermind!   #")
    print("##############################")
    print()

    cm = CodeMaker()

    print(
        "I am the CodeMaker and I have prepared {pegs}-peg pattern using {colors} different colors (letters)."
        .format(
            pegs=cm.pegs_number,
            colors=cm.colors_number,
        )
    )
    print(
        "You are the CodeBreaker and you have {turns}"
        .format(
            turns=cm.turns_limit,
        ),
        "turn" if cm.turns_limit == 1 else "turns",
        "to guess the solution pattern."
    )
    print()

    while not cm.game_status:
        try:
            print(cm.input_for_codemaker(input(cm.prompt)))
        except ValueError as err:
            print(err)
    print()

    if cm.game_status == 1:
        print(
            "You found the solution in {turns}"
            .format(
                turns=cm.turns_counter,
            ),
            "turn." if cm.turns_counter == 1 else "turns."
        )
    elif cm.game_status == 2:
        print("You reached turns limit. Game over!")

    print(
        "The solution pattern is {pattern}."
        .format(
            pattern=cm.solution_pattern,
        )
    )


if __name__ == "__main__":
    main()
