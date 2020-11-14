########################################
# My version of famous game Mastermind #
# h.py                                 #
# Mastermind Helper shortcut           #
#             Piotr Loos (c) 2019-2020 #
########################################

from helper import MastermindHelper


MastermindHelper(
    colors_number=8,
    pegs_number=8,
    turns_limit=0,
    shuffle_before=False,
    shuffle_after=False,
    solver_mode=2,
    progress_timing=True,
    mode1_second_solution=True,
    mode2_random_pattern=False,
)
