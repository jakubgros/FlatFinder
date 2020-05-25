import unittest

from comparators.morphologic_comparator import MorphologicComparator


class MorphologicComparatorTest(unittest.TestCase):

    def setUp(self):
        self.comparator = MorphologicComparator()

    def test_1_word_comparison(self):
        self.assertTrue(self.comparator.equals("Stanisława", "Stanisławem"))
        self.assertFalse(self.comparator.equals("Piotra", "Stanisławem"))

    def test_2_words_comparison(self):
        self.assertTrue(self.comparator.equals("Stanisława Krasickiego", "Stanisławem Krasickim"))
        self.assertFalse(self.comparator.equals("Piotr Krasicki", "Stanisławem Ignacym Krasickim"))

    def test_3_words_comparison(self):
        self.comparator = MorphologicComparator()
        self.assertTrue(self.comparator.equals("Stanisława Ignacego Krasickiego", "Stanisławem Ignacym Krasickim"))
        self.assertFalse(self.comparator.equals("Stanisława Piotra Krasickiego", "Stanisławem Ignacym Krasickim"))

    def test_case_insensitive_comparison(self):
        self.assertTrue(self.comparator.equals("stanisława", "Stanisława"))
        self.assertTrue(self.comparator.equals("stanisława", "STANISłAWA"))

    def test_title_case_sensitive_comparison(self):
        comparator = MorphologicComparator(title_case_sensitive=True)

        self.assertTrue(comparator.equals("Stanisława Kowalska", "Stanisławy Kowalskiej"))
        self.assertTrue(comparator.equals("STANISŁAWY KOWALSKIEJ", "STANISŁAWY KOWALSKIEJ"))
        self.assertTrue(comparator.equals("stanisława kowalska", "stanisławy kowalskiej"))

        self.assertFalse(comparator.equals("Stanisława Kowalska", "stanisławy kowalskiej"))
        self.assertFalse(comparator.equals("Stanisława Kowalska", "STANISŁAWY KOWALSKIEJ"))

    def test_ignore_title_case_sensitive_comparison_if_actual_is_upper_case(self):
        c = MorphologicComparator(title_case_sensitive=True,
                                  ignore_case_sensitivity_if_actual_upper_case=True)

        self.assertFalse(c.equals("Stanisława Kowalska", "stanisławy kowalskiej"))
        self.assertTrue(c.equals("Stanisława Kowalska", "STANISŁAWY KOWALSKIEJ"))
        self.assertFalse(c.equals("STANISŁAWY KOWALSKIEJ", "Stanisława Kowalska"))  # only works if actual is uppercase

    def test_comparison_ignores_white_spaces(self):
        self.assertTrue(self.comparator.equals("jakieś słowo  ", "    jakieś    słowo"))

    def test_comparison_ignores_white_spaces(self):
        self.assertTrue(self.comparator.equals("jakieś słowo  ", "    jakieś    słowo"))


if __name__ == "__main__":
    unittest.main()
