import unittest

from containers.morphologic_set import MorphologicSet


class MorphologicSetTest(unittest.TestCase):
    def test_in_operator(self):
        morph_set = MorphologicSet(['doktor'])
        self.assertTrue('doktora' in morph_set)
        self.assertTrue('doktorem' in morph_set)
        self.assertTrue('doktorów' in morph_set)
        self.assertTrue('dr' in morph_set)
        self.assertTrue('profesor' not in morph_set)


if __name__ == '__main__':
    unittest.main()
