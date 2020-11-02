#Do not invoke main.py to run, use "py UnittestExercises.py" instead.

import unittest


class TestSum(unittest.TestCase):

    def test_sum_list(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_typle(self):
        self.assertEqual(sum((1, 2, 3)), 6, "Should be 6")

    def test_none(self):
        self.assertIsNone(None, "Should be None")

    def test_a(self):
        self.assertIsInstance(, int, "Should be int")

if __name__ == "__main__":
    unittest.main()