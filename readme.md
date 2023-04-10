# mastermind
## My version of the famous Mastermind game

Hi there! I'm glad you're interested in my coding project.
The Mastermind game is quite simple but entertaining code, to present my skills in pure Python 3, e.g.:

* OOP principles - encapsulation, polymorphism
* class inheritance, overriding methods, abstract methods, meta classes
* method properties, decorators, class and static methods
* iterators, generators, map and lambda functions
* list comprehensions
* exception raises and catches, assertions
* context managers
* tuple, dict and function arguments (\*args, \*\*kwargs) unpacking
* colored output in terminal
* PEP 8, DRY, KISS, YAGNI, code comments

## Rules

Mastermind is a code-breaking game for two players. In my program one of the players is computer.
One player becomes the codemaker, the other the codebreaker. The codemaker chooses a pattern of 4 pegs (by default) using 6 different color pegs (by default).
The solution pattern is visible to the codemaker, but not to the codebreaker.

The codebreaker tries to guess the pattern, in both order and color, within 12 turns (by default).
Each guess is made by entering a row (pattern) of colored pegs into terminal.
Once placed, the codemaker provides a response by placing from 0 to 4 response pegs nearby the row with the guess.
A black peg is placed for each code peg from the guess which is correct in both color and position.
A white peg indicates the existence of a correct color peg placed in the wrong position.
Once response is provided, another guess is made.
Guesses and responses continue to alternate until either the codebreaker guesses correctly, or reaches the turns limit.
In computer solving modes the game also could end after being convinced that there is no possible solution based on user provided responses.

## Modes

* game

* solver

* helper

## Solvers

* Solver #1 = patterns checking generator Solver

* Solver #2 = patterns list filtering Solver

## Settings

In my game you can specify various settings that affects a game. They are grouped into 5 categories.

### Terminal settings

* `bool` **styled_prints** (default value `False` - for compatibility). When enabled the most of terminal prints will be formatted using colors, bolds, underlines, frames etc. Use only when your terminal supports this function, otherwise the output would be unreadable.

* `bool` **use_digits_for_colors** (default value `True`). Describes the way how to input/output colors for pegs. When enabled the program uses digits from `1`-`10` (digit `0` means `10` value) and then letters (almost like in hexadecimal number system). The minimum pattern is then `1111`. When disabled the program uses only letters (starting from `a`), so the minimum patterns is `aaaa`.

* `bool` **progress_timing** (default value `True`). Enables the time measurements for long taking operations and prints the result after finish.

* `bool` **print_settings_list** (default value `False`). Enables printing the list of all settings before starting a game. Additional information for advanced users.

* `bool` **print_guesses_list** (default value `True`). Enables printing the list of all guesses so far after each game turn.

### Mastermind settings

* `int` **peg_colors** (default value `6`). Main Mastermind setting. The number of different peg colors to be used in patterns (from `2` to `24`). The more color pegs there are, the harder the game is.

* `int` **pegs_in_pattern** (default value `4`). Main Mastermind setting. The number of ordered pegs in one pattern (from `2` to `16`). The more pegs there are in the pattern, the harder the game is.

* `bool` **allow_blanks** (default value `False`). Not implemented yet! In future you will be able to enable blank pegs for guesses, the ones that cannot occur in solution pattern for sure.

* `bool` **allow_duplicates** (default value `True`). Not implemented yet! In future you will be able to disable duplicating color pegs in pattern. Both for guesses and for solution pattern.

* `int` **guesses_limit** (default value `12`). The number of guesses the codebreaker has to reveal the solution. Set to `0` if you want to have an unlimited play.

### Solving settings

* `int` **chosen_solver** (default value `1`). Choose index of the implemented Solvers. #1 = patterns checking generator Solver, #2 = patterns list filtering Solver. They are described above.

* `bool` **pre_build_patterns** (default value `False`). Enables building possible patterns list for several games at once. Useful when you play several games one by one using the same settings. This setting can take a lot of RAM to keep all the patterns in memory. When disabled the patterns will be generated real-time during computer solving, but it can be slower and not efficient from the Mastermind's point of view (list of the patterns cannot be shuffled).

* `bool` **use_itertools_for_build** (default value `True`). Enables Python built-in itertools module to generate patterns. It is a bit faster than my generating function, but it doesn't handle all shuffling settings below.

* `bool` **shuffle_colors_before_build** (default value `False`). Enables one-time color pegs order shuffling before pattern generation is started. It doesn't change the efficiency of guessing, but allows not to start always with the first minimum (the same one color) pattern.

* `bool` **shuffle_colors_during_build** (default value `False`). Enables color pegs order shuffling for every peg in pattern. It can improve the efficiency of guessing, when the codebreaker starts from mixed color pattern. This setting is unused when itertools module is used.

* `bool` **shuffle_patterns_after_build** (default value `False`). Enables one-time patterns order shuffling after the pattern list is built. You can achieve the best guessing efficiency, but first you must pre build patterns and keep them in memory. Patterns shuffling is impossible for pattern real-time generators. In Solver #2 you can use instead `solver2_take_random_pattern` setting which is faster.

### Solver #1 settings

* `bool` **solver1_calc_2nd_solution** (default value `True`). Enables searching for second possible solution after finding the first one. Using this setting Solver #1 can sometimes be sure that current guess is the only one possible solution (and it's not a guess in fact).

### Solver #2 settings

* `bool` **solver2_take_random_pattern** (default value `False`). Enables taking random pattern from the possible solutions list, which is more efficient from the Mastermind's point of view. It is similar to `shuffle_patterns_after_build` setting, but it can be used only for Solver #2, which has the whole list. When disabled Solver #2 takes the first possible solution from the list.

* `int` **solver2_print_possible_solutions_threshold** (default value `10`). Sets the maximum number of patterns in the possible solutions list, which will be printed after filtering the list. You can see patterns which still can be a solution after each turn. Set to `0` if you want to disable this printing.

### Note

Please keep in mind that not every settings combinations are possible. You won't get an error, however some less significant settings will be omitted.
