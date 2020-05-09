import unittest

from src.morfeusz import Morfeusz

class MorfeuszTest(unittest.TestCase):

    def setUp(self):
        self.morfeusz = Morfeusz.Instance()

    def test_3_words_comparison(self):
        self.assertTrue(self.morfeusz.equals("Stanisława Ignacego Krasickiego", "Stanisławem Ignacym Krasickim"))
        self.assertFalse(self.morfeusz.equals("Stanisława Piotra Krasickiego", "Stanisławem Ignacym Krasickim"))

    def test_2_words_comparison(self):
        self.assertTrue(self.morfeusz.equals("Stanisława Krasickiego", "Stanisławem Krasickim"))
        self.assertFalse(self.morfeusz.equals("Piotr Krasicki", "Stanisławem Ignacym Krasickim"))

    def test_1_word_comparison(self):
        self.assertTrue(self.morfeusz.equals("Stanisława", "Stanisławem"))
        self.assertFalse(self.morfeusz.equals("Piotra", "Stanisławem"))

    def test_comparison_is_case_insensitive(self):
        self.assertTrue(self.morfeusz.equals("stanisława", "Stanisława"))
        self.assertTrue(self.morfeusz.equals("stanisława", "STANISłAWA"))

    def test_comparison_ignores_accents(self):
        self.assertTrue(self.morfeusz.equals("żółć", "żółci"))

    def test_comparison_ignores_white_spaces(self):
        self.assertTrue(self.morfeusz.equals("jakieś słowo  ", "    jakieś    słowo"))


if __name__ == "__main__":
    unittest.main() # run all tests