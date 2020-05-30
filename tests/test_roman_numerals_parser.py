import unittest

from parsers.roman_numerals_parser import RomanNumeralsParser


class RomanNumeralsParserTest(unittest.TestCase):

    def test_roman_numbers_are_correctly_recognized(self):
        self.assertTrue(RomanNumeralsParser.is_roman_number("I"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("II"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("III"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("IV"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("V"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("VI"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("VII"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("VIII"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("IX"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("X"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XI"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XII"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XIII"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XVI"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XV"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XVI"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XVII"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XVIII"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XIX"))
        self.assertTrue(RomanNumeralsParser.is_roman_number("XX"))

    def test_lower_case_roman_numbers_are_not_recognized_as_valid_values(self):
        self.assertFalse(RomanNumeralsParser.is_roman_number("i"))
        self.assertFalse(RomanNumeralsParser.is_roman_number("ii"))
        self.assertFalse(RomanNumeralsParser.is_roman_number("v"))
        self.assertFalse(RomanNumeralsParser.is_roman_number("d"))
        self.assertFalse(RomanNumeralsParser.is_roman_number("c"))
        self.assertFalse(RomanNumeralsParser.is_roman_number("x"))

    def test_no_other_characters_are_accepted(self):
        self.assertFalse(RomanNumeralsParser.is_roman_number("Mieszka I"))
        self.assertFalse(RomanNumeralsParser.is_roman_number(" I "))
        self.assertFalse(RomanNumeralsParser.is_roman_number("-I"))
        self.assertFalse(RomanNumeralsParser.is_roman_number("I,"))
        self.assertFalse(RomanNumeralsParser.is_roman_number("I."))

    def test_to_arabic(self):
        self.assertTrue(RomanNumeralsParser.to_arabic("I"), 1)
        self.assertTrue(RomanNumeralsParser.to_arabic("II"), 2)
        self.assertTrue(RomanNumeralsParser.to_arabic("III"), 3)
        self.assertTrue(RomanNumeralsParser.to_arabic("IV"), 4)
        self.assertTrue(RomanNumeralsParser.to_arabic("V"), 5)
        self.assertTrue(RomanNumeralsParser.to_arabic("VI"), 6)
        self.assertTrue(RomanNumeralsParser.to_arabic("VII"), 7)
        self.assertTrue(RomanNumeralsParser.to_arabic("VIII"), 8)
        self.assertTrue(RomanNumeralsParser.to_arabic("IX"), 9)
        self.assertTrue(RomanNumeralsParser.to_arabic("X"), 10)
        self.assertTrue(RomanNumeralsParser.to_arabic("XI"), 11)
        self.assertTrue(RomanNumeralsParser.to_arabic("XII"), 12)
        self.assertTrue(RomanNumeralsParser.to_arabic("XIII"), 13)
        self.assertTrue(RomanNumeralsParser.to_arabic("XVI"), 14)
        self.assertTrue(RomanNumeralsParser.to_arabic("XV"), 15)
        self.assertTrue(RomanNumeralsParser.to_arabic("XVI"), 16)
        self.assertTrue(RomanNumeralsParser.to_arabic("XVII"), 17)
        self.assertTrue(RomanNumeralsParser.to_arabic("XVIII"), 18)
        self.assertTrue(RomanNumeralsParser.to_arabic("XIX"), 19)
        self.assertTrue(RomanNumeralsParser.to_arabic("XX"), 20)


if __name__ == "__main__":
    unittest.main()
