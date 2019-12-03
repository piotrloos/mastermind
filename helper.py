from mastermind import Mastermind

game = Mastermind(pegs=7, colors=10)

result = None
while result != (game.pegs, 0):

    try:
        pattern = next(game.hint_generator())
    except StopIteration:
        print("No solution!")
        break

    result = tuple(int(peg) for peg in input("{} -> ".format(pattern)).split())
    game.guesses[pattern] = result

print("Solution pattern is {}".format(pattern))
