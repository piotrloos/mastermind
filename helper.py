########################################
# My version of famous game Mastermind #
# helper.py                            #
# Game helper file                     #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import Mastermind


def main():
    """ Main I/O file for Mastermind Helper """

    print()
    print("Welcome to Mastermind Helper!")
    game = Mastermind(generate=False, pegs=4, colors=6, max_tries=2)
    print("You have prepared {}-peg pattern using {} colors.".format(game.pegs, game.colors))
    print("I have {} tries to guess the solution.".format(game.max_tries))
    print()

    pattern = None
    game.hint = game.hint_generator(shuffle=True)

    while game.active:

        try:
            pattern = next(game.hint)
        except StopIteration:
            print("No solution found!")
            game.active = False
            break

        while True:
            # format(game.counter, tuple(map(lambda x: chr(x+96), pattern)))
            result = game.input_result(input("{}: {} -> ".format(game.counter, pattern)))

            if result is None:
                print("Incorrect result value. Enter again.")
            else:
                # print("{}: {} -> {}".format(game.counter, pattern, result))
                game.add_result(pattern, result)
                break

    print()
    if game.won:
        print("The solution pattern is {}".format(pattern))
        print("I found the solution in {}".format(game.counter), "guesses." if game.counter > 1 else "guess.")
    else:
        print("Reached guess limit. Game over!")


if __name__ == "__main__":
    main()
