# mastermind
My version of the famous Mastermind game

Hi there! I'm glad you're interested in my coding project.
The Mastermind game is quite simple but entertaining code, to present my skills in pure Python 3 like:
* OOP principles - encapsulation, polymorphism
* class inheritance, overriding methods, abstract methods, metaclasses
* method properties, decorators, class and static methods
* exception raising and catching, assertions
* iterators, generators, map and lambda functions
* list comprehensions
* context managers
* tuple and function arguments unpacking
* colored output in terminal
* PEP 8, DRY, KISS, YAGNI, code comments

## Rules

Mastermind is a code-breaking game for two players. In my program one of the players is computer.
One player becomes the codemaker, the other the codebreaker. The codemaker chooses a pattern of 4 pegs (by default) using 6 different color pegs (by default).
The solution pattern is visible to the codemaker, but not to the codebreaker.

The codebreaker tries to guess the pattern, in both order and color, within 12 turns (by default).
Each guess is made by placing a row of colored pegs on the decoding board.
Once placed, the codemaker provides a response by placing from 0 to 4 response pegs in the small holes of the row with the guess.
A black peg is placed for each code peg from the guess which is correct in both color and position.
A white peg indicates the existence of a correct color peg placed in the wrong position.
Once response is provided, another guess is made.
Guesses and responses continue to alternate until either the codebreaker guesses correctly, or reaches the turns limit.

## Modes

* game
* solver
* helper

## Settings

In my game you can specify various settings that affects a game.

### Terminal settings

* styled_prints
* use_digits_for_colors
* progress_timing
* print_settings_list
* print_guesses_list

### Mastermind settings

* peg_colors
* pegs_in_pattern
* allow_blanks
* allow_duplicates
* guesses_limit

### Solving settings

* chosen_solver
* pre_build_patterns
* use_itertools_for_build
* shuffle_colors_before_build
* shuffle_colors_during_build
* shuffle_patterns_after_build

### Solver #1 settings

* solver1_calc_2nd_solution

### Solver #2 settings

* solver2_take_random_pattern
* solver2_print_possible_solutions_threshold
