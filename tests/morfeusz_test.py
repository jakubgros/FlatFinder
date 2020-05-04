import unittest

from src.morfeusz import Morfeusz

class MorfeuszTest(unittest.TestCase):

    def setUp(self):
        self.morfeusz = Morfeusz()

    def test_3_words_comparison(self):
        self.assertTrue(self.morfeusz.compare("Stanisława Ignacego Krasickiego", "Stanisławem Ignacym Krasickim"))
        self.assertFalse(self.morfeusz.compare("Stanisława Piotra Krasickiego", "Stanisławem Ignacym Krasickim"))

    def test_2_words_comparison(self):
        self.assertTrue(self.morfeusz.compare("Stanisława Krasickiego", "Stanisławem Krasickim"))
        self.assertFalse(self.morfeusz.compare("Piotr Krasicki", "Stanisławem Ignacym Krasickim"))

    def test_1_word_comparison(self):
        self.assertTrue(self.morfeusz.compare("Stanisława", "Stanisławem"))
        self.assertFalse(self.morfeusz.compare("Piotra", "Stanisławem"))

    def test_comparison_is_case_insensitive(self):
        self.assertTrue(self.morfeusz.compare("stanisława", "Stanisława"))
        self.assertTrue(self.morfeusz.compare("stanisława", "STANISłAWA"))

    def test_comparison_ignores_accents(self):
        self.assertTrue(self.morfeusz.compare("żółć", "żółci"))

    def test_comparison_ignores_white_spaces(self):
        self.assertTrue(self.morfeusz.compare("jakieś słowo  ", "    jakieś    słowo"))


if __name__ == "__main__":
    unittest.main() # run all tests