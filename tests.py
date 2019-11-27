########################################
# My version of famous game Mastermind #
# tests.py                             #
# Unittests for mastermind             #
########################################

import unittest
from mastermind import Game


class GameCreationTests(unittest.TestCase):
    """ Testing class for creations new game """
    def test_new_game_with_correct_pattern(self):
        pattern = (1, 2, 3, 4)
        a = Game(pattern)
        self.assertTupleEqual(a.reveal_pattern(), pattern)

    def test_new_game_without_given_pattern(self):
        a = Game()
        self.assertTrue(a.validate_pattern(a.reveal_pattern()))

    def test_new_game_with_incorrect_pattern1(self):
        with self.assertRaises(ValueError):
            Game(2)

    def test_new_game_with_incorrect_pattern2(self):
        with self.assertRaises(ValueError):
            Game((1, 2, 3))

    def test_new_game_with_incorrect_pattern3(self):
        with self.assertRaises(ValueError):
            Game((6, 6, 5, 7))

    def test_new_game_with_incorrect_pattern4(self):
        with self.assertRaises(ValueError):
            Game((6, 6, 5.4, 5))

    def test_new_game_with_incorrect_pattern5(self):
        with self.assertRaises(ValueError):
            Game((6, 6, "a", 5))
