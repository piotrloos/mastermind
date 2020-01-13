########################################
# My version of famous game Mastermind #
# solver.py                            #
# CodeBreaker I/O file                 #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import CodeBreaker


def main():
    """ Main I/O file for Mastermind CodeBreaker """

    print()
    print("##############################")
    print("#   Welcome to Mastermind!   #")
    print("##############################")
    print()

    cb = CodeBreaker(colors=8, pegs=5, hint_mode=0)

    print(
        "You are the CodeMaker and you have prepared {pegs}-peg pattern using {colors} different colors (letters)."
        .format(
            pegs=cb.pegs_number,
            colors=cb.colors_number,
        )
    )
    print(
        "I am the CodeBreaker and I have {turns}"
        .format(
            turns=cb.turns_limit,
        ),
        "turn" if cb.turns_limit == 1 else "turns",
        "to guess the solution pattern."
    )
    print(
        "Example pattern is {pattern}."
        .format(
            pattern=cb.example_pattern,
        )
    )
    print()

    while not cb.game_status:
        try:
            print(cb.input_for_codebreaker(input(cb.prompt)))
        except ValueError as err:
            print(err)
    print()

    if cb.game_status == 1:
        print(
            "The solution pattern is {pattern}."
            .format(
                pattern=cb.current_pattern,
            )
        )
        print(
            "I found the solution in {turns}"
            .format(
                turns=cb.turns_counter,
            ),
            "turn." if cb.turns_counter == 1 else "turns."
        )
    elif cb.game_status == 2:
        print("I reached turns limit. Game over!")
    elif cb.game_status == 3:
        print("Sorry. No possible solution found!")


if __name__ == "__main__":
    main()
