import unittest
from word_frequency_sol import *

class TestCase(unittest.TestCase):
    def test_1(self):
        assert word_frequency([]) == {}
    def test_2(self):
        assert word_frequency(["apple", "banana", "apple", "orange", "banana", "apple"]) == {'apple': 3, 'banana': 2, 'orange': 1}
    def test_3(self):
        assert word_frequency(["cat", "dog", "cat", "bird", "cat", "dog", "fish"]) == {'cat': 3, 'dog': 2, 'bird': 1, 'fish': 1}
    def test_4(self):
        assert word_frequency(["apple", "banana", "apple", "orange", "banana", "apple", "Apple", "Orange"]) == {'apple': 3, 'banana': 2, 'orange': 1, 'Apple': 1, 'Orange': 1}


if __name__ == "__main__":
    test_result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestCase))

    if test_result.wasSuccessful():
        print("All tests passed successfully! Ready to submit solution.")