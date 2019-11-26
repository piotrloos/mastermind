import unittest
from mastermind import Game


class GameCreationTests(unittest.TestCase):
    def test_new_game_with_correct_code(self):
        code = [1, 2, 3, 4]
        a = Game(code)
        self.assertListEqual(a.reveal(), code)

    def test_new_game_without_given_code(self):
        Game()
        self.assertTrue(True)

    def test_new_game_with_incorrect_code1(self):
        with self.assertRaises(ValueError):
            Game(2)

    def test_new_game_with_incorrect_code2(self):
        with self.assertRaises(ValueError):
            Game([1, 2, 3])

    def test_new_game_with_incorrect_code3(self):
        with self.assertRaises(ValueError):
            Game([6, 6, 5, 7])

    def test_new_game_with_incorrect_code4(self):
        with self.assertRaises(ValueError):
            Game([6, 6, 5.4, 5])

    def test_new_game_with_incorrect_code5(self):
        with self.assertRaises(ValueError):
            Game([6, 6, "a", 5])
