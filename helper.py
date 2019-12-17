########################################
# My version of famous game Mastermind #
# helper.py                            #
# Game helper file                     #
#                  Piotr Loos (c) 2019 #
########################################

from mastermind import Helper


def main():
    """ Main I/O file for Mastermind Helper """

    print()
    print("Welcome to Mastermind Helper!")
    helper = Helper(colors=8, pegs=7, hint_mode=0)
    print("You have prepared {}-peg pattern using {} colors.".format(helper.pegs, helper.colors))
    print("I have {}".format(helper.max_tries), "try" if helper.max_tries == 1 else "tries", "to guess the solution.")
    print()

    while not helper.status:
        if helper.input_result(input(helper.prompt())):
            print("Incorrect result value. Enter again.")

    print()
    if helper.status == 1:
        print("The solution pattern is {}.".format(helper.print_pattern(helper.current_pattern)))
        print("I found the solution in {}".format(helper.counter), "try." if helper.counter == 1 else "tries.")
    elif helper.status == 2:
        print("I reached tries limit. Game over!")
    elif helper.status == 3:
        print("No possible solution found!")


if __name__ == "__main__":
    main()
