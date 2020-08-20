########################################
# My version of famous game Mastermind #
# helper.py                            #
# Mastermind Helper I/O file           #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import MastermindHelper


def main():
    """ Main I/O file for Mastermind Helper """

    print()
    print("#####################################")
    print("#   Welcome to Mastermind Helper!   #")
    print("#####################################")
    print()

    mh = MastermindHelper(colors=8, pegs=6, shuffle_before=False, shuffle_after=False, solve_mode=2)

    print()
    print(
        "You are the CodeBreaker and somebody has prepared {pegs}-peg pattern using {colors} different colors: {list}."
        .format(
            pegs=mh.pegs_number,
            colors=mh.colors_number,
            list=mh.colors_list,
        )
    )
    print(
        "I am the Helper and I have {turns}"
        .format(
            turns=mh.turns_limit,
        ),
        "turn" if mh.turns_limit == 1 else "turns",
        "to help you guess the solution pattern."
    )
    print(
        "There are {number} possible patterns in this game. Example pattern is {pattern}."
        .format(
            number=mh.patterns_number,
            pattern=mh.get_random_pattern(),
        )
    )
    print(
        "Settings: shuffle_before = {shuffle_before}, shuffle_after = {shuffle_after}, solve_mode = {solve_mode}."
        .format(
            shuffle_before=mh.shuffle_before,
            shuffle_after=mh.shuffle_after,
            solve_mode=mh.solve_mode,
        )
    )
    print()

    while not mh.game_status:
        try:
            mh.helper_take_turn(input(mh.helper_prompt))
        except ValueError as err:
            print(err)
    print()

    if mh.game_status == 1:
        print(
            "The solution is {pattern}."
            .format(
                pattern=mh.solution,
            )
        )
        print(
            "You found the solution in {turns}"
            .format(
                turns=mh.turns_counter,
            ),
            "turn." if mh.turns_counter == 1 else "turns."
        )
    elif mh.game_status == 2:
        print("You reached turns limit. Game over!")
    elif mh.game_status == 3:
        print("Sorry. No possible solution found!")

    print("Thanks for playing!")


if __name__ == "__main__":
    main()
