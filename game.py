########################################
# My version of famous game Mastermind #
# game.py                              #
# Main file                            #
########################################

from mastermind import Mastermind


def main():
    """ Main I/O function """

    print("Welcome in my Mastermind!")
    game = Mastermind((1, 2, 3, 4))
    print("Generated {} pegs pattern from {} colors.".format(game.pegs, game.colors))
    print("You have {} tries to guess the pattern.".format(game.tries))

    while not game.game_finished:

        pattern = game.input_pattern(input("Guess number {}: ".format(game.guess_count)))
        if game.validate_pattern(pattern):
            print("{}: {} -> {}".format(game.guess_count, pattern, game.guess_pattern(pattern)))
        else:
            print("Incorrect pattern. Try again.")

    if game.game_won:
        print("You won in {}".format(game.guess_count),
              "guesses." if game.guess_count > 1 else "guess. Congratulations!"
              )
    else:
        print("You reached guess limit. Unfortunately you lost.")


if __name__ == "__main__":
    main()
