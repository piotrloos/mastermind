########################################
# My version of famous game Mastermind #
# helper.py                            #
# Game helper file                     #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import Mastermind


def main():
    """ Main I/O file for helper """

    print()
    print("Welcome in my Mastermind helper!")
    game = Mastermind(generate=False, pegs=7, colors=10)
    print("Searching for {}-peg solution using {} colors.".format(game.pegs, game.colors))
    print()

    result = None
    pattern = None
    game.hint = game.hint_generator()

    while result != (game.pegs, 0):

        try:
            pattern = next(game.hint)
        except StopIteration:
            print("No solution!")
            game.active = False
            break

        result = game.input_result(input("{} -> ".format(pattern)))
        game.guesses[pattern] = result

    if game.active:
        print("Solution pattern is {}".format(pattern))


if __name__ == "__main__":
    main()
