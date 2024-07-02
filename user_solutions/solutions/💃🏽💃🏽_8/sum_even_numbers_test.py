import unittest
from sum_even_numbers_sol import *

class TestCase(unittest.TestCase):
    def test_1(self):
        assert sum_even_numbers([2, 4, 6, 8, 10]) == 30
    def test_2(self):
        assert sum_even_numbers([1, 3, 5, 7, 9]) == 0
    def test_3(self):
        assert sum_even_numbers([2, 3, 5, 7, 11]) == 2
    def test_4(self):
        assert sum_even_numbers([-2, -4, 0, 2, 3, 5, 7, 11, 1000]) == 996


if __name__ == "__main__":
    test_result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestCase))

    if test_result.wasSuccessful():
        print("All tests passed successfully! Ready to submit solution.")