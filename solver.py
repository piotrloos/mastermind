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

    ms = MastermindSolver(
        colors_number=8,
        pegs_number=6,
        shuffle_before=False,
        shuffle_after=False,
        solver_mode=2,
    )

    print()
    print(
        "You are the CodeMaker and you have prepared {pegs}-peg pattern using {colors} different colors: {list}."
        .format(
            pegs=ms.settings.pegs_number,
            colors=ms.settings.colors_number,
            list=ms.settings.pegs_list,
        )
    )
    print(
        "I am the CodeBreaker and I have {turns}"
        .format(
            turns=ms.settings.turns_limit,
        ),
        "turn" if ms.settings.turns_limit == 1 else "turns",
        "to guess the solution pattern."
    )
    print(
        "There are {number} possible patterns in this game. Example pattern is {pattern}."
        .format(
            number=ms.settings.patterns_number,
            pattern=ms.get_random_pattern(),
        )
    )
    print(
        "Settings: shuffle_before = {shuffle_before}, shuffle_after = {shuffle_after}, solver_mode = {solver_mode}."
        .format(
            shuffle_before=ms.settings.shuffle_before,
            shuffle_after=ms.settings.shuffle_after,
            solver_mode=ms.settings.solver_mode,
        )
    )
    print()

    while not ms.game_status:
        try:
            ms.solver_take_turn(input(ms.solver_prompt))
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
