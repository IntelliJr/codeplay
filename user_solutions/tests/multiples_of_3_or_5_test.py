import unittest
from multiples_of_3_or_5_sol import *

class TestCase(unittest.TestCase):
    def test_1(self):
        assert multiples_of_3_or_5(10) == 23
    def test_2(self):
        assert multiples_of_3_or_5(1000) == 233168
    def test_3(self):
        assert multiples_of_3_or_5(-1) == 0
    def test_4(self):
        assert multiples_of_3_or_5(0) == 0

if __name__ == "__main__":
    test_result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestCase))

    if test_result.wasSuccessful():
        print("All tests passed successfully! Ready to submit solution.")