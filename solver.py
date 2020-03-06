########################################
# My version of famous game Mastermind #
# solver.py                            #
# Mastermind Solver I/O file           #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import MastermindSolver


def main():
    """ Main I/O file for Mastermind Solver """

    print()
    print("#####################################")
    print("#   Welcome to Mastermind Solver!   #")
    print("#####################################")
    print()

    ms = MastermindSolver(colors=7, pegs=8, shuffle_mode=1, solve_mode=1)

    print()
    print(
        "You are the CodeMaker and you have prepared {pegs}-peg pattern using {colors} different colors: {list}."
        .format(
            pegs=ms.pegs_number,
            colors=ms.colors_number,
            list=ms.colors_list,
        )
    )
    print(
        "I am the CodeBreaker and I have {turns}"
        .format(
            turns=ms.turns_limit,
        ),
        "turn" if ms.turns_limit == 1 else "turns",
        "to guess the solution pattern."
    )
    print(
        "There are {number} possible patterns in this game. Example pattern is {pattern}."
        .format(
            number=ms.patterns_number,
            pattern=ms.example_pattern,
        )
    )
    print(
        "Shuffle MODE is set to {shuffle} and Solver MODE is set to {solve}."
        .format(
            shuffle=ms.shuffle_mode,
            solve=ms.solve_mode,
        )
    )
    print()

    while not ms.game_status:
        try:
            ms.take_turn_human(input(ms.prompt))
        except ValueError as err:
            print(err)
    print()

    if ms.game_status == 1:
        print(
            "The solution is {pattern}."
            .format(
                pattern=ms.solution,
            )
        )
        print(
            "I found the solution in {turns}"
            .format(
                turns=ms.turns_counter,
            ),
            "turn." if ms.turns_counter == 1 else "turns."
        )
    elif ms.game_status == 2:
        print("I reached turns limit. Game over!")
    elif ms.game_status == 3:
        print("Sorry. No possible solution found!")

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
