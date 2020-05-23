import unittest

from text.analysis.morphologic_analyser import MorphologicAnalyser
from comparators.morphologic_comparator import MorphologicComparator


class MorfeuszTest(unittest.TestCase):

    def setUp(self):
        self.morfeusz = MorphologicAnalyser.Instance()

    def test_3_words_comparison(self):
        self.assertTrue(MorphologicComparator.equals("Stanisława Ignacego Krasickiego", "Stanisławem Ignacym Krasickim"))
        self.assertFalse(MorphologicComparator.equals("Stanisława Piotra Krasickiego", "Stanisławem Ignacym Krasickim"))

    def test_2_words_comparison(self):
        self.assertTrue(MorphologicComparator.equals("Stanisława Krasickiego", "Stanisławem Krasickim"))
        self.assertFalse(MorphologicComparator.equals("Piotr Krasicki", "Stanisławem Ignacym Krasickim"))

    def test_1_word_comparison(self):
        self.assertTrue(MorphologicComparator.equals("Stanisława", "Stanisławem"))
        self.assertFalse(MorphologicComparator.equals("Piotra", "Stanisławem"))

    def testcomparison_is_case_insensitive(self):
        self.assertTrue(MorphologicComparator.equals("stanisława", "Stanisława"))
        self.assertTrue(MorphologicComparator.equals("stanisława", "STANISłAWA"))

    def test_comparison_ignores_accents(self):
        self.assertTrue(MorphologicComparator.equals("żółć", "żółci"))

    def test_comparison_ignores_white_spaces(self):
        self.assertTrue(MorphologicComparator.equals("jakieś słowo  ", "    jakieś    słowo"))

    def test_data_extension(self):
        # data for Bonerowska flection has been extended manually
        self.assertTrue(MorphologicComparator.equals("Bonerowska", "Bonerowskiej"))

    def test_reinterpret(self):
        # morfeusz doesn't recognize oś as osiedle. We force it to reinterpret oś as osiedle and do the analysis using Morfeusz library
        self.assertTrue(MorphologicComparator.equals("oś", "osiedle"))


if __name__ == "__main__":
    unittest.main() # run all tests