import unittest

from utilities.utilities import split_on_special_characters


class TestUtilities(unittest.TestCase):

    def test_split_preserves_newline_character(self):
        sample_text = "this is a \n sample text"
        word_list = split_on_special_characters(sample_text, preserve_special_characters=True)
        self.assertIn('\n', word_list)

if __name__ == '__main__':
    unittest.main()
