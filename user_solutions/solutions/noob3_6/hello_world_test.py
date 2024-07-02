#import os
import unittest
from hello_world_sol import *

#os.chdir("user_solutions/solutions")

class TestCase(unittest.TestCase):
    def test_1(self):
        assert hello_world() == "Hello World"

if __name__ == "__main__":
    test_result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestCase))

    if test_result.wasSuccessful():
        print("All tests passed successfully! Ready to submit solution.")