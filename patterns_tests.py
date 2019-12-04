from random import sample, shuffle


def product(*args):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    # args = list(range(3))
    # pools = map(tuple, args*2)
    # print(*args)
    result = [[]]
    for pool in map(tuple, args*3):
        result = [x+[y] for x in result for y in sample(pool, len(pool))]
        # print(pool, "$$$", result)
    shuffle(result)
    # print()
    for pattern in result:
        yield tuple(pattern)


def product2(pegs=4, colors=6):
    patterns = [[]]
    for _ in range(pegs):
        patterns = ((*x, y) for x in patterns for y in sample(range(1, colors + 1), colors))
    for pattern in patterns:
        yield pattern


i = 0
for a in product2():
    i += 1
    print(a)
print(i)
