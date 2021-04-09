import unittest
import calculator

class TestCalculator(unittest.TestCase):

    def test_add(self):
        result = calculator.add_func(10, 5)
        self.assertEqual(result, 15)