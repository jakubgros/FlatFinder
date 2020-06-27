import unittest

from text.preprocessors.english_description_remover import EnglishDescriptionRemover
from utilities.utilities import split_on_special_characters


class TestEnglishDescriptionRemover(unittest.TestCase):

    def test_removing_english_part(self):
        polish_txt = "To jest jakiś tekst po polsku, razem ze specjalnymi. Znakami itp..."
        english_txt = "And this is a sample text,\n this time in English."

        remover = EnglishDescriptionRemover()
        without_english = remover.process(polish_txt + " " + english_txt)
        self.assertEqual(polish_txt, without_english)


if __name__ == '__main__':
    unittest.main()
