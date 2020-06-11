import unittest

from utilities.utilities import split_on_special_characters, find_slice_beg, do_slices_overlap, strip_list


class TestSplitOnSpecialCharacters(unittest.TestCase):

    def test_split_preserves_newline_character(self):
        sample_text = "this is a \n sample text"
        word_list = split_on_special_characters(sample_text, preserve_special_characters=True)
        self.assertIn('\n', word_list)


class TestFindSlice(unittest.TestCase):

    def test_find_single_elem(self):
        self.assertEqual(0, find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[1, 2]))
        self.assertEqual(1, find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[2, 3]))
        self.assertEqual(2, find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[3, 4]))
        self.assertEqual(3, find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[4, 5]))

        self.assertEqual(0, find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[1]))
        self.assertEqual(4, find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[5]))

        self.assertEqual(0, find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[1, 2, 3, 4, 5]))

    def test_find_not_existing(self):
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[]))
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[5, 6]))
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[7, 8]))
        self.assertIsNone(find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[1, 3]))

    def test_find_all(self):
        self.assertEqual([0], find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[1], find_all=True))
        self.assertEqual([2], find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[3], find_all=True))
        self.assertEqual([4], find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[5], find_all=True))

        self.assertEqual([0, 2, 4], find_slice_beg([1, 2, 1, 4, 1], slice_to_find=[1], find_all=True))

        self.assertEqual([], find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[], find_all=True))
        self.assertEqual([], find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[6], find_all=True))
        self.assertEqual([], find_slice_beg([1, 2, 3, 4, 5], slice_to_find=[6, 7], find_all=True))

    def test_find_case_insensitive(self):
        self.assertIsNotNone(find_slice_beg(["Nieopodal"], slice_to_find=["nieopodal"], case_insensitive=True))


class TestDoSlicesOverlap(unittest.TestCase):

    def test_empty_slices(self):
        self.assertFalse(do_slices_overlap((0, 0), (0, 0)))
        self.assertFalse(do_slices_overlap((1, 1), (1, 1)))

    def test_comparison_is_commutative(self):
        self.assertTrue(do_slices_overlap((0, 2), (1, 2)))
        self.assertTrue(do_slices_overlap((1, 2), (0, 2)))

    def test_overlapping_slices(self):
        self.assertTrue(do_slices_overlap((0, 2), (1, 2)))
        self.assertTrue(do_slices_overlap((0, 4), (1, 2)))
        self.assertTrue(do_slices_overlap((0, 4), (0, 4)))

    def test_not_overlapping_slices(self):
        self.assertFalse(do_slices_overlap((0, 4), (3, 3)))
        self.assertFalse(do_slices_overlap((0, 4), (4, 4)))
        self.assertFalse(do_slices_overlap((0, 4), (4, 5)))


class TestStripList(unittest.TestCase):

    def test_strip(self):
        self.assertEqual([True],
                         strip_list([False, False, True, False], strip_if_in=[False]))

        self.assertEqual([True, True],
                         strip_list([False, True, True, False], strip_if_in=[False]))

        self.assertEqual([True, True, True],
                         strip_list([False, True, True, True], strip_if_in=[False]))

        self.assertEqual([True, True, True],
                         strip_list([True, True, True, False], strip_if_in=[False]))

        self.assertEqual([True, True, True],
                         strip_list([True, True, True, False], strip_if_in=[False]))

        self.assertEqual([True, True, True, True],
                         strip_list([True, True, True, True], strip_if_in=[False]))

    def test_strip_all(self):
        self.assertEqual([],
                         strip_list([False, False, False, False], strip_if_in=[False]))

    def test_empty_list(self):
        self.assertEqual([],
                         strip_list([], strip_if_in=[False]))

        self.assertEqual([],
                         strip_list([], strip_if_in=[]))

    def test_strip_multiple_values(self):
        self.assertEqual([3, 4, 5, 6],
                         strip_list([1, 2, 3, 4, 5, 6, 1, 2], strip_if_in=[1, 2]))


if __name__ == '__main__':
    unittest.main()
