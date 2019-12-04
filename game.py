########################################
# My version of famous game Mastermind #
# game.py                              #
# Main game file                       #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import Mastermind


def main():
    """ Main I/O file for game """

    print()
    print("Welcome in my Mastermind!")
    game = Mastermind()
    print("Generated {}-peg pattern using {} colors.".format(game.pegs, game.colors))
    print("You have {} tries to guess the solution.".format(game.max_tries))
    print()

    while game.active:

        pattern = game.input_pattern(input("Guess number {}: ".format(game.tries_counter)))

        if pattern is None:
            print("Incorrect pattern. Try again.")
        else:
            print("{}: {} -> {}".format(game.tries_counter, pattern, game.guess(pattern)))
            print()

    if game.won:
        print("You won in {}".format(game.tries_counter),
              "guesses." if game.tries_counter > 1 else "guess. Congratulations!"
              )
    else:
        print("You reached guess limit. Unfortunately you lost.")
        print("The solution pattern was {}.".format(game.reveal_solution()))


if __name__ == "__main__":
    main()
