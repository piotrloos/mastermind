########################################
# My version of famous game Mastermind #
# game.py                              #
# Main file                            #
########################################

from mastermind import Mastermind


def main():
    """ Main I/O function """

    print("Welcome in my Mastermind!")
    game = Mastermind((2, 2, 3, 3))
    print("Generated {} pegs pattern from {} colors.".format(game.pegs, game.colors))
    pattern = None

    while not game.game_finished:

        try:
            pattern = tuple(int(x) for x in input("Guess number {}: ".format(game.guess_count + 1)).split())
        except ValueError:
            pass

        if game.validate_pattern(pattern):
            print("{}: {} -> {}".format(game.guess_count + 1, pattern, game.guess_pattern(pattern)))
        else:
            print("Incorrect pattern. Try again.")

    if game.game_won:
        print("You won in {}".format(game.guess_count),
              "guesses." if game.guess_count > 1 else "guess. Congratulations!"
              )
    else:
        print("Unfortunately you lost.")


if __name__ == "__main__":
    main()
