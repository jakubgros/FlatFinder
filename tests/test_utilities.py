import unittest

from utilities.utilities import split_on_special_characters, find_slice_beg


class TestSplitOnSpecialCharacters(unittest.TestCase):

    def test_split_preserves_newline_character(self):
        sample_text = "this is a \n sample text"
        word_list = split_on_special_characters(sample_text, preserve_special_characters=True)
        self.assertIn('\n', word_list)


class TestFindSlice(unittest.TestCase):

    def test_find_single_elem(self):
        self.assertEqual(0, find_slice_beg([1, 2, 3, 4, 5], [1, 2]))
        self.assertEqual(1, find_slice_beg([1, 2, 3, 4, 5], [2, 3]))
        self.assertEqual(2, find_slice_beg([1, 2, 3, 4, 5], [3, 4]))
        self.assertEqual(3, find_slice_beg([1, 2, 3, 4, 5], [4, 5]))

        self.assertEqual(0, find_slice_beg([1, 2, 3, 4, 5], [1]))
        self.assertEqual(4, find_slice_beg([1, 2, 3, 4, 5], [5]))

        self.assertEqual(0, find_slice_beg([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]))

    def test_find_not_existing(self):
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], []))
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], [5, 6]))
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], [7, 8]))
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], [1, 3]))

    def test_find_all(self):
        self.assertEqual([0], find_slice_beg([1, 2, 3, 4, 5], [1], find_all=True))
        self.assertEqual([2], find_slice_beg([1, 2, 3, 4, 5], [3], find_all=True))
        self.assertEqual([4], find_slice_beg([1, 2, 3, 4, 5], [5], find_all=True))

        self.assertEqual([0, 2, 4], find_slice_beg([1, 2, 1, 4, 1], [1], find_all=True))

        self.assertEqual([], find_slice_beg([1, 2, 3, 4, 5], [], find_all=True))
        self.assertEqual([], find_slice_beg([1, 2, 3, 4, 5], [6], find_all=True))
        self.assertEqual([], find_slice_beg([1, 2, 3, 4, 5], [6, 7], find_all=True))

    def test_find_case_insensitive(self):
        self.assertIsNotNone(find_slice_beg(["Nieopodal"], ["nieopodal"], case_insensitive=True))


if __name__ == '__main__':
    unittest.main()
