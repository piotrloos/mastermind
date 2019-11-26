from random import randint

PEGS = 4


class Game:
    def __init__(self, code=None):
        if code is None:
            self.pattern = [randint(1, 6) for _ in range(PEGS)]
        else:
            if not isinstance(code, list) or len(code) != PEGS:
                raise ValueError("Incorrect code.")
            self.pattern = code

    def reveal(self):
        print(self.pattern)


a = Game()
a.reveal()

b = Game([1, 2, 3, 4])
b.reveal()

try:
    c = Game(2)
except ValueError:
    print("c error")

try:
    d = Game([1, 2, 3])
except ValueError:
    print("d error")
