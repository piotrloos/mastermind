########################################
# My version of famous game Mastermind #
# solver.py                            #
# Mastermind Solver I/O file           #
#             Piotr Loos (c) 2019-2020 #
########################################

from mastermind import MastermindSolver


def main():
    """ Main I/O file for Mastermind Solver """

    ms = MastermindSolver(
        colors_number=8,
        pegs_number=8,
        turns_limit=0,
        shuffle_before=False,
        shuffle_after=False,
        solver_mode=1,
        progress_timing=True,
        mode1_second_solution=True,
        mode2_random_pattern=False,
    )

    ms.solver_intro()

    while not ms.game_status:
        try:
            ms.solver_take_turn(input(ms.solver_prompt))
        except ValueError as err:
            print(err)

    ms.solver_outro()


if __name__ == "__main__":
    main()
