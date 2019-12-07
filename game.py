########################################
# My version of famous game Mastermind #
# game.py                              #
# Main game file                       #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import Mastermind


def main():
    """ Main I/O file for Mastermind Game """

    print()
    print("Welcome to Mastermind Game!")
    game = Mastermind()
    print("I have prepared {}-peg pattern using {} colors.".format(game.pegs, game.colors))
    print("You have {} tries to guess the solution.".format(game.max_tries))
    print()

    while game.active:

        pattern = game.input_pattern(input("{}: ".format(game.counter)))

        if pattern is None:
            print("Incorrect pattern. Enter again.")
        else:
            print("{}: {} -> {}".format(game.counter, pattern, game.add_pattern(pattern)))

    print()
    if game.won:
        print("You found the solution in {}".format(game.counter), "guesses." if game.counter > 1 else "guess.")
    else:
        print("Reached guess limit. Game over!")

    print("The solution pattern is {}. Thanks for playing!".format(game.solution))


if __name__ == "__main__":
    main()
