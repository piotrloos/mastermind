########################################
# My version of famous game Mastermind #
# tests.py                             #
# Unittests for mastermind             #
#                  Piotr Loos (c) 2019 #
########################################

import unittest
from mastermind import Mastermind


class MastermindCreationTests(unittest.TestCase):
    """ Testing class for creations new game with standard settings """

    def test_new_game_with_correct_pattern(self):
        pattern = (1, 2, 3, 4)
        a = Mastermind(pattern)
        self.assertTrue(a.active)
        self.assertTupleEqual(a.reveal_solution(), pattern)
        self.assertFalse(a.active)

    def test_new_game_without_given_pattern(self):
        a = Mastermind()
        self.assertTrue(a.active)
        self.assertTrue(a.validate(a.reveal_solution()))
        self.assertFalse(a.active)

    def test_new_game_with_incorrect_pattern1(self):
        with self.assertRaises(ValueError):
            Mastermind(2)

    def test_new_game_with_incorrect_pattern2(self):
        with self.assertRaises(ValueError):
            Mastermind((1, 2, 3))

    def test_new_game_with_incorrect_pattern3(self):
        with self.assertRaises(ValueError):
            Mastermind((6, 6, 5, 7))

    def test_new_game_with_incorrect_pattern4(self):
        with self.assertRaises(ValueError):
            Mastermind((6, 6, 5.4, 5))

    def test_new_game_with_incorrect_pattern5(self):
        with self.assertRaises(ValueError):
            Mastermind((6, 6, "a", 5))


class CustomGameCreationTests(unittest.TestCase):
    """ Testing class for creations new game with custom settings """

    def test_new_game_with_more_pegs_number(self):
        pattern = (1, 2, 3, 4, 5)
        a = Mastermind(pattern, pegs=5)
        self.assertTupleEqual(a.reveal_solution(), pattern)

    def test_new_game_with_less_pegs_number(self):
        pattern = (1, 2)
        a = Mastermind(pattern, pegs=2)
        self.assertTupleEqual(a.reveal_solution(), pattern)

    def test_new_game_with_incorrect_pegs_number(self):
        pattern = (1,)
        with self.assertRaises(ValueError):
            Mastermind(pattern, pegs=1)

    def test_new_game_with_more_colors_number(self):
        pattern = (1, 2, 7, 8)
        a = Mastermind(pattern, colors=8)
        self.assertTupleEqual(a.reveal_solution(), pattern)

    def test_new_game_with_less_colors_number(self):
        pattern = (1, 2, 1, 2)
        a = Mastermind(pattern, colors=2)
        self.assertTupleEqual(a.reveal_solution(), pattern)

    def test_new_game_with_incorrect_colors_number(self):
        pattern = (1, 1, 1, 1)
        with self.assertRaises(ValueError):
            Mastermind(pattern, colors=1)

    def test_new_game_with_custom_correct_settings(self):
        pattern = (8, 4, 1, 3, 8, 5)
        a = Mastermind(pattern, pegs=6, colors=8)
        self.assertTupleEqual(a.reveal_solution(), pattern)

    def test_new_game_with_custom_incorrect_settings1(self):
        pattern = (4, 7, 5, 2, 8)
        with self.assertRaises(ValueError):
            Mastermind(pattern, pegs=7, colors=8)

    def test_new_game_with_custom_incorrect_settings2(self):
        pattern = (4, 7, 5, 2, 8)
        with self.assertRaises(ValueError):
            Mastermind(pattern, pegs=5, colors=7)

    def test_new_game_with_custom_incorrect_settings3(self):
        pattern = (4, 7, 5, 2, 8)
        with self.assertRaises(ValueError):
            Mastermind(pattern, pegs=3, colors=4)


class PegsCalculateTests(unittest.TestCase):
    """ Testing class for calculate black and white pegs """

    def setUp(self):
        self.a = Mastermind(solution=(2, 8, 8, 3, 5, 3), pegs=6, colors=10, max_tries=20)

    def test_example_game(self):
        self.assertTrue(self.a.active)
        self.assertTupleEqual(self.a.guess((1, 6, 9, 7, 10, 4)), (0, 0))
        self.assertTupleEqual(self.a.guess((1, 6, 5, 6, 8, 4)), (0, 2))
        self.assertTupleEqual(self.a.guess((9, 2, 3, 7, 2, 10)), (0, 2))
        self.assertTupleEqual(self.a.guess((8, 8, 10, 5, 10, 3)), (2, 2))
        self.assertTupleEqual(self.a.guess((3, 8, 10, 10, 1, 5)), (1, 2))
        self.assertTupleEqual(self.a.guess((5, 4, 10, 8, 3, 8)), (0, 4))
        self.assertTupleEqual(self.a.guess((10, 5, 8, 9, 5, 8)), (2, 1))
        self.assertTupleEqual(self.a.guess((7, 7, 8, 3, 8, 5)), (2, 2))
        self.assertTupleEqual(self.a.guess((2, 8, 6, 3, 5, 3)), (5, 0))
        self.assertTupleEqual(self.a.guess((8, 3, 2, 5, 3, 8)), (0, 6))
        self.assertTrue(self.a.active)
        self.assertTupleEqual(self.a.guess((2, 8, 8, 3, 5, 3)), (6, 0))
        self.assertFalse(self.a.active)
