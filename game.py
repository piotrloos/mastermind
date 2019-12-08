########################################
# My version of famous game Mastermind #
# game.py                              #
# Main game file                       #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import Game


def main():
    """ Main I/O file for Mastermind Game """

    print()
    print("Welcome to Mastermind Game!")
    game = Game()
    print("I have prepared {}-peg pattern using {} colors.".format(game.pegs, game.colors))
    print("You have {}".format(game.max_tries), "try" if game.max_tries == 1 else "tries", "to guess the solution.")
    print()

    while not game.status:

        pattern = game.input_pattern(input("{}: ".format(game.counter)))

        if pattern is None:
            print("Incorrect pattern. Enter again.")
        else:
            print("{}: {} -> {}".format(game.counter, pattern, game.add_pattern(pattern)))

    print()
    if game.status == 1:
        print("You found the solution in {}".format(game.counter), "try." if game.counter == 1 else "tries.")
    elif game.status == 2:
        print("You reached tries limit. Game over!")

    print("The solution pattern is {}.".format(game.solution))


if __name__ == "__main__":
    main()
