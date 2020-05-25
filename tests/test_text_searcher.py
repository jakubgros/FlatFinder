import unittest

from text.TextSearcher import TextSearcher


class TestTextSearcher(unittest.TestCase):
    def test_text_searcher_correctly_handles_incorrect_spacing(self):
        # hyphen should be surrounded by spaces
        self.assertTrue(TextSearcher.contains("Armii Krajowej", "Armii Krajowej-na skrzyżowaniu"))


if __name__ == '__main__':
    unittest.main()
