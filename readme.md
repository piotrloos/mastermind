# mastermind

## My version of the famous Mastermind game

Hi there! I'm glad you're interested in my coding project.
The Mastermind game is quite simple but entertaining code, to present my skills in pure Python 3, e.g.:

* OOP principles - encapsulation, polymorphism
* class inheritance, overriding methods, abstract methods, meta classes
* method properties, decorators, class and static methods
* Python closures
* iterators, generators, map and lambda functions
* list comprehensions
* exceptions raises and catches, assertions
* context managers
* tuple, dict and function arguments (\*args, \*\*kwargs) unpacking
* colored output in terminal
* PEP 8, DRY, KISS, YAGNI, code comments

## Mastermind rules

Mastermind is a code-breaking game for two players. In my program one of the players is the computer.
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

## Mastermind modes

* **`game`**: In this mode the codemaker is the computer - prepares the solution pattern and returns you the responses. The codebreaker is you - you enter the patterns and try to guess the solution. Since you are the one who guesses, choosing a Solver and defining his settings is unnecessary.

* **`solver`**: In this mode the codemaker is you - you have prepared the solution pattern and you give the computer responses for every guess. The codebreaker is the computer and he guesses the pattern using one of the two different Solvers #1 or #2 (described below). Sometimes the computer is sure that his guess is the proper solution and tells you about it.

* **`helper`**: In this mode the computer helps you to guess the solution pattern when you are playing with someone else. Very similar to `solver` mode. You enter every guess you made and his response, and then the computer gives you one of the possible solutions using the same Solvers as in `solver` mode. You can enter any pattern and response, or just a response based on the previously proposed pattern.

## Solvers

* **`Solver #1`** = patterns checking generator Solver. This Solver generates patterns one by one and checks if they satisfy every previous guess and his response. After the pattern is passed to codemaker and the response is received Solver continue scanning for the next possible solutions. Therefore, at the beginning of the game this Solver can quickly make guesses, as the solving time raises when the game reaches the end. This Solver doesn't need patterns to be generated before starting a game, so he doesn't consume so much memory as `Solver #2`. Also, this Solver can search for second possible solution (see `solver1_calc_2nd_solution` setting) to be sure that the first found is the only one possible.

* **`Solver #2`** = patterns list filtering Solver. This Solver prepares list of all possible solutions (which can take a lot of memory) and reduces it after each guess. So, first turns can take some time, but the closer the solution this Solver is, the faster he can give possible solutions. This Solver can be more efficient from the Mastermind's point of view than `Solver #1`, because he can take random pattern from the list (see `solver2_take_random_pattern` setting) and get the response that rejects more patterns. Additionally, this Solver can print the remaining possible solutions list (see `solver2_print_possible_solutions_threshold` setting) if there are only few of them.

* **`Solver #3`** = logic thinking Solver using constraint module. Not implemented yet!

## Settings

In my game you can specify various settings that affects a game. They are grouped into 5 categories.

### Terminal settings

* _(bool)_ **`styled_prints`** (default value `False` - for compatibility). When enabled the most of terminal prints will be formatted using colors, bolds, underlines, frames etc. Use only when your terminal supports this function, otherwise the output would be unreadable.

* _(bool)_ **`use_digits_for_colors`** (default value `True`). Describes the way how to input/output colors for pegs. When enabled the program uses digits from `1`-`10` (digit `0` means `10` value) and then letters (almost like in hexadecimal number system). The minimum pattern is then `1111`. When disabled the program uses only letters (starting from `a`), so the minimum patterns is `aaaa`.

* _(bool)_ **`progress_timing`** (default value `True`). Enables the time measurements for long taking operations and prints the result after finish.

* _(bool)_ **`print_settings_list`** (default value `False`). Enables printing the list of all settings before starting a game. Additional information for advanced users.

* _(bool)_ **`print_guesses_list`** (default value `True`). Enables printing the list of all guesses so far after each game turn.

### Mastermind settings

* _(int)_ **`peg_colors`** (default value `6`). Main Mastermind setting. The number of different peg colors to be used in patterns (from `2` to `24`). The more color pegs there are, the harder the game is.

* _(int)_ **`pegs_in_pattern`** (default value `4`). Main Mastermind setting. The number of ordered pegs in one pattern (from `2` to `16`). The more pegs there are in the pattern, the harder the game is.

* _(bool)_ **`allow_blanks`** (default value `False`). Not implemented yet! In future you will be able to enable blank pegs for guesses, the ones that cannot occur in solution pattern for sure.

* _(bool)_ **`allow_duplicates`** (default value `True`). Not implemented yet! In future you will be able to disable duplicating color pegs in pattern. Both for guesses and for solution pattern.

* _(int)_ **`guesses_limit`** (default value `12`). The number of guesses the codebreaker has to reveal the solution. Set to `0` if you want to have an unlimited play.

### Solving settings

* _(int)_ **`chosen_solver`** (default value `1`). Choose index of the implemented Solvers. #1 = patterns checking generator Solver, #2 = patterns list filtering Solver. They are described above. In `game` mode this and related settings are unnecessary.

* _(bool)_ **`pre_build_patterns`** (default value `False`). Enables building possible patterns list for several games at once. Useful when you play several games one by one using the same settings. This setting can take a lot of RAM to keep all the patterns in memory. When disabled the patterns will be generated real-time during computer solving, but it can be slower and not efficient from the Mastermind's point of view (list of the patterns cannot be shuffled).

* _(bool)_ **`use_itertools_for_build`** (default value `True`). Enables Python built-in itertools module to generate patterns. It is a bit faster than my generating function, but it doesn't handle all shuffling settings below.

* _(bool)_ **`shuffle_colors_before_build`** (default value `False`). Enables one-time color pegs order shuffling before pattern generation is started. It doesn't change the efficiency of guessing, but allows not to start always with the first minimum (the same one color) pattern.

* _(bool)_ **`shuffle_colors_during_build`** (default value `False`). Enables color pegs order shuffling for every peg in pattern. It can improve the efficiency of guessing, when the codebreaker starts from mixed color pattern. This setting is unused when itertools module is used.

* _(bool)_ **`shuffle_patterns_after_build`** (default value `False`). Enables one-time patterns order shuffling after the pattern list is built. You can achieve the best guessing efficiency, but first you must pre build patterns and keep them in memory. Patterns shuffling is impossible for pattern real-time generators. In Solver #2 you can use instead `solver2_take_random_pattern` setting which is faster.

### Solver #1 settings

* _(bool)_ **`solver1_calc_2nd_solution`** (default value `True`). Enables searching for second possible solution after finding the first one. Using this setting Solver #1 can sometimes be sure that current guess is the only one possible solution (and it's not a guess in fact).

### Solver #2 settings

* _(bool)_ **`solver2_take_random_pattern`** (default value `False`). Enables taking random pattern from the possible solutions list, which is more efficient from the Mastermind's point of view. It is similar to `shuffle_patterns_after_build` setting, but it can be used only for Solver #2, which has the whole list. When disabled Solver #2 takes the first possible solution from the list.

* _(int)_ **`solver2_print_possible_solutions_threshold`** (default value `10`). Sets the maximum number of patterns in the possible solutions list, which will be printed after filtering the list. You can see patterns which still can be a solution after each turn. Set to `0` if you want to disable this printing. If there is only one possible solution in the list, the computer knows that it must be a solution.

### Note

Please keep in mind that not every settings combinations are possible. You won't get an error, however some less significant settings will be omitted.

## Running

Just launch `./main.py`. Most of the settings are set, for some important you will be asked.
If you don't want to be asked you can give some settings as a parameter launching a program in any order, e.g.:

```
./main.py mode=solver peg_colors=8 pegs_in_pattern=6 chosen_solver=2 pre_build_patterns=1 use_itertools_for_build=0 solver2_take_random_pattern=1 styled_prints=1
```

Running `main.py` you will be asked if you want to play again after the current game is ended. The settings will be the same. If there were patterns generated they will not be generated again.

You can also manually call once the proper Mastermind class

* MastermindGame()
* MastermindSolver()
* MastermindHelper()

giving some keywords arguments. For example:

```
MastermindSolver(
    peg_colors=8,
    pegs_in_pattern=6,
    chosen_solver=2,
    pre_build_patterns=True,
    use_itertools_for_build=False,
    solver2_take_random_pattern=True,
    styled_prints=True,
)
```

## Have fun :)

Piotr Loos (c) 2023
