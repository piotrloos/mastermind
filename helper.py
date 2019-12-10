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
    helper = Helper(colors=6, pegs=4, hints_sample_mode=2)
    print("You have prepared {}-peg pattern using {} colors.".format(helper.pegs, helper.colors))
    print("I have {}".format(helper.max_tries), "try" if helper.max_tries == 1 else "tries", "to guess the solution.")
    print()

    pattern = None

    while not helper.status:

        pattern = helper.get_hint()
        if pattern is None:
            break

        while True:
            result = helper.input_result(input("{}: {} -> ".format(helper.counter, helper.print_pattern(pattern))))

            if result is None:
                print("Incorrect result value. Enter again.")
            else:
                helper.add_result(pattern, result)
                break

    print()
    if helper.status == 1:
        print("The solution pattern is {}.".format(helper.print_pattern(pattern)))
        print("I found the solution in {}".format(helper.counter), "try." if helper.counter == 1 else "tries.")
    elif helper.status == 2:
        print("I reached tries limit. Game over!")
    elif helper.status == 3:
        print("No possible solution found!")


if __name__ == "__main__":
    main()
