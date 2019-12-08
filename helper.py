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
    game = Mastermind(generate=False, colors=10, pegs=6, hints_sample_mode=0)
    print("You have prepared {}-peg pattern using {} colors.".format(game.pegs, game.colors))
    print("I have {}".format(game.max_tries), "try" if game.max_tries == 1 else "tries", "to guess the solution.")
    print()

    pattern = None
    game.hint = game.hint_generator()

    while not game.status:

        try:
            pattern = next(game.hint)
        except StopIteration:
            game.status = 3
            break

        while True:
            # map(lambda x: chr(x+96), pattern)
            result = game.input_result(input("{}: {} -> ".format(game.counter, pattern)))

            if result is None:
                print("Incorrect result value. Enter again.")
            else:
                game.add_result(pattern, result)
                break

    print()
    if game.status == 1:
        print("The solution pattern is {}".format(pattern))
        print("I found the solution in {}".format(game.counter), "try." if game.counter == 1 else "tries.")
    elif game.status == 2:
        print("I reached tries limit. Game over!")
    elif game.status == 3:
        print("No possible solution found!")


if __name__ == "__main__":
    main()
