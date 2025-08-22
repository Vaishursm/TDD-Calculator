import unittest
from string_calculator import StringCalculator

class TestStringCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = StringCalculator()

    def test_empty_string_returns_zero(self):
        self.assertEqual(self.calc.add(""), 0)

    def test_single_number(self):
        self.assertEqual(self.calc.add("5"), 5)

    def test_two_numbers_comma_delimited(self):
        self.assertEqual(self.calc.add("1,2"), 3)

    def test_two_numbers_newline_delimited(self):
        self.assertEqual(self.calc.add("1\n2"), 3)

    def test_three_numbers_mixed_delimiters(self):
        self.assertEqual(self.calc.add("1\n2,3"), 6)

    def test_custom_delimiter(self):
        self.assertEqual(self.calc.add("//;\n1;2"), 3)

    def test_negative_numbers_raise(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.add("1,-2,3,-4")
        self.assertIn("negatives not allowed", str(ctx.exception))

    def test_numbers_greater_than_1000_ignored(self):
        self.assertEqual(self.calc.add("2,1001"), 2)

    def test_long_delimiter(self):
        self.assertEqual(self.calc.add("//[***]\n1***2***3"), 6)

    def test_multiple_delimiters(self):
        self.assertEqual(self.calc.add("//[*][%]\n1*2%3"), 6)

    def test_called_count(self):
        self.calc.add("1,2")
        self.calc.add("3")
        self.assertEqual(self.calc.get_called_count(), 2)

if __name__ == "__main__":
    unittest.main()
