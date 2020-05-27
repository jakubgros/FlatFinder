import unittest

from text.text_frame import TextFrame


class TestTextFrame(unittest.TestCase):

    def _test_helper(self, all_words_list, frame, expected_text):
        frame = list(frame)
        self.assertEqual(len(frame), len(expected_text))

        for (frame_slice, frame_text), expected_text in zip(frame, expected_text):
            self.assertEqual(frame_text, expected_text)
            self.assertEqual(" ".join(all_words_list[slice(*frame_slice)]), expected_text)

    def test_text_frame(self):
        word_list = "a sample text".split()
        self._test_helper(word_list, TextFrame(word_list, 1), ['a', 'sample', 'text'])
        self._test_helper(word_list, TextFrame(word_list, 2), ['a sample', 'sample text'])
        self._test_helper(word_list, TextFrame(word_list, 3), ['a sample text'])
        self._test_helper(word_list, TextFrame(word_list, 4), [])


if __name__ == '__main__':
    unittest.main()
