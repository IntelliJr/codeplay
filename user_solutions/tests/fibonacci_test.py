import unittest
from fibonacci_sol import *

class TestCase(unittest.TestCase):
    def test_1(self):
        assert fibonacci(1) == 0
    def test_2(self):
        assert fibonacci(2) == 1
    def test_3(self):
        assert fibonacci(3) == 1
    def test_4(self):
        assert fibonacci(5) == 3
    def test_5(self):
        assert fibonacci(7) == 8
    def test_6(self):
        assert fibonacci(16) == 610
    def test_7(self):
        assert fibonacci(-1) == -1
    def test_8(self):
        assert fibonacci(0.1) == -1

if __name__ == "__main__":
    test_result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestCase))

    if test_result.wasSuccessful():
        print("All tests passed successfully! Ready to submit solution.")