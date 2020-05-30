from roman import fromRoman, InvalidRomanNumeralError


class RomanNumeralsParser:
    @staticmethod
    def to_arabic(roman_as_str):
        """ returns integer arabic number equal to provided roman number
        throws InvalidRomanNumeralError in case provided value is not valid roman number
        """
        return fromRoman(roman_as_str)

    @staticmethod
    def is_roman_number(roman_as_str):
        """ returns True in case provided value is valid roman number, False otherwise """
        try:
            fromRoman(roman_as_str)
        except InvalidRomanNumeralError:
            return False
        else:
            return True
