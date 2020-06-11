import unittest

from comparators.morphologic_comparator import MorphologicComparator
from text.text_searcher import TextSearcher


class TestTextSearcher(unittest.TestCase):

    def test_text_searcher_correctly_handles_incorrect_spacing(self):
        # hyphen should be surrounded by spaces
        found, *_ = TextSearcher.find(phrase_to_find="Armii Krajowej", text="Armii Krajowej-na skrzyżowaniu")
        self.assertTrue(found)

    def test_special_characters_are_not_ignored(self):
        found, *_ = TextSearcher.find(phrase_to_find="Armii Krajowej", text="na ulicy Armii, Krajowej")
        self.assertFalse(found)

        found, *_ = TextSearcher.find(phrase_to_find="Armii Krajowej", text="na ulicy Armii Krajowej")
        self.assertTrue(found)

    def test_custom_comparators(self):
        eq_comparator = MorphologicComparator().equals
        to_find = "Nowy Kleparz"

        found, *_ = TextSearcher.find(phrase_to_find=to_find,
                                      text="na Nowym Kleparzu",
                                      equality_comparator=eq_comparator)
        self.assertTrue(found)

        found, *_ = TextSearcher.find(phrase_to_find=to_find,
                                      text="lokalizacja Nowy Kleparz",
                                      equality_comparator=eq_comparator)
        self.assertTrue(found)

        found, *_ = TextSearcher.find(phrase_to_find=to_find,
                                      text="niedaleko od Nowego Kleparza",
                                      equality_comparator=eq_comparator)
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
