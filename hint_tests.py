from mastermind import Mastermind

# try:
#     print(next(c))
# except StopIteration:
#     print("stop 1")
#
# try:
#     print(next(c))
# except StopIteration:
#     print("stop 2")

# b = Mastermind((5, 2, 3, 4))
b = Mastermind()

# c = b.hint_generator()
# print(len([x for x in c]))

# for _ in range(3):
#     print(next(c))
# print()

# b.guess_pattern((4, 2, 5, 1))
c = b.hint_generator()

# print(len([x for x in c]))

# for _ in range(3):
#     print(next(c))
# print()

b.guess(next(c))
# b.guess_pattern((4, 4, 4, 4))
c = b.hint_generator()

# print(len([x for x in c]))

# for _ in range(3):
#     print(next(c))
# print()

b.guess(next(c))
# b.guess_pattern((5, 2, 3, 4))

c = b.hint_generator()
b.guess(next(c))

c = b.hint_generator()
b.guess(next(c))

c = b.hint_generator()
print(len([x for x in c]))

# for _ in range(3):
#     print(next(c))
# print()
