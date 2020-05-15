import unittest

from src.name_comparator import NameComparator


class NameComparatorTest(unittest.TestCase):
    def testNameWithoutTitleEqualsNameWithTitle(self):
        comparator = NameComparator()
        self.assertTrue(comparator.equals("ks. Jana Kowalskiego", "Jana Kowalskiego"))
