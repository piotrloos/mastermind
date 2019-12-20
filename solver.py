########################################
# My version of famous game Mastermind #
# solver.py                            #
# CodeBreaker file                     #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import CodeBreaker


def main():
    """ Main I/O file for Mastermind CodeBreaker """

    print()
    print("Welcome to Mastermind!")
    cb = CodeBreaker(colors=8, pegs=6, hint_mode=0)
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
            turns=cb.turns_limit
        ),
        "turn" if cb.turns_limit == 1 else "turns",
        "to guess the solution pattern."
    )
    print()

    while not cb.game_status:
        if cb.input_for_codebreaker(input(cb.prompt)):
            print("Incorrect response. Enter again.")

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
