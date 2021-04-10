import unittest
import calculator
import json

class TestCalculator(unittest.TestCase):

    def test_add(self):
        resultAdd = calculator.add_func(10, 5)
        self.assertEqual(resultAdd, 15)
    
    def test_subtract(self):
        resultSub = calculator.subtract_func(10, 5)
        self.assertEqual(resultSub, 5)

if __name__ == '__main__':
    unittest.main()