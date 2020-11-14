########################################
# My version of famous game Mastermind #
# s.py                                 #
# Mastermind Solver shortcut           #
#             Piotr Loos (c) 2019-2020 #
########################################

from solver import MastermindSolver


MastermindSolver(
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
