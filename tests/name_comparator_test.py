import unittest

from src.name_comparator import NameComparator


class NameComparatorTest(unittest.TestCase):
    def testTitleIgnoringFirstNameAndSurnameComparison(self):
        test_cases = [
            ("ks. Jana Kowalskiego", "Jana Kowalskiego"),
            ("księdza Jana Kowalskiego", "Jana Kowalskiego"),
            ("abp. Jana Kowalskiego", "Jana Kowalskiego"),
            ("arcybiskupa Jana Kowalskiego", "Jana Kowalskiego"),
            ("gen. Jana Kowalskiego", "Jana Kowalskiego"),
            ("generała Jana Kowalskiego", "Jana Kowalskiego"),
            ("generał Anny Kowalskiej", "Anny Kowalskiej"),
            ("marsz. Jana Kowalskiego", "Jana Kowalskiego"),
            ("marszałka Jana Kowalskiego", "Jana Kowalskiego"),
            ("marszałek Anny Kowalskiej", "Anny Kowalskiej"),
            ("płk. Jana Kowalskiego", "Jana Kowalskiego"),
            ("pułkownika Jana Kowalskiego", "Jana Kowalskiego"),
            ("pułkownik Anny Kowalskiej", "Anny Kowalskiej"),
            ("bł. Jana Kowalskiego", "Jana Kowalskiego"),
            ("błogosławionego Jana Kowalskiego", "Jana Kowalskiego"),
            ("błogosławionej Anny Kowalskiej", "Anny Kowalskiej"),
            ("bp. Jana Kowalskiego", "Jana Kowalskiego"),
            ("bpa Jana Kowalskiego", "Jana Kowalskiego"),
            ("biskupa Jana Kowalskiego", "Jana Kowalskiego"),
            ("dr Jana Kowalskiego", "Jana Kowalskiego"),
            ("doktora Jana Kowalskiego", "Jana Kowalskiego"),
            ("doktor Anny Kowalskiej", "Anny Kowalskiej"),
            ("pil. Jana Kowalskiego", "Jana Kowalskiego"),
            ("pilota Jana Kowalskiego", "Jana Kowalskiego"),
            ("harc. Jana Kowalskiego", "Jana Kowalskiego"),
            ("harcmistrza Jana Kowalskiego", "Jana Kowalskiego"),
            ("prof. Jana Kowalskiego", "Jana Kowalskiego"),
            ("profesora Jana Kowalskiego", "Jana Kowalskiego"),
            ("profesor Anny Kowalskiej", "Anny Kowalskiej"),
            ("kmr. Jana Kowalskiego", "Jana Kowalskiego"),
            ("komandora Jana Kowalskiego", "Jana Kowalskiego"),
            ("króla Jana Kowalskiego", "Jana Kowalskiego"),
            ("królowej Anny Kowalskiej", "Anny Kowalskiej"),
            ("kard. Jana Kowalskiego", "Jana Kowalskiego"),
            ("kardynała Jana Kowalskiego", "Jana Kowalskiego"),
            ("księcia Jana Kowalskiego", "Jana Kowalskiego"),
            ("mjr. Jana Kowalskiego", "Jana Kowalskiego"),
            ("majora Jana Kowalskiego", "Jana Kowalskiego"),
            ("matki Anny Kowalskiej", "Anny Kowalskiej"),
            ("o. Jana Kowalskiego", "Jana Kowalskiego"),
            ("ojca Jana Kowalskiego", "Jana Kowalskiego"),
            ("por. Jana Kowalskiego", "Jana Kowalskiego"),
            ("porucznika Jana Kowalskiego", "Jana Kowalskiego"),
            ("rtm. Jana Kowalskiego", "Jana Kowalskiego"),
            ("rotmistrza Jana Kowalskiego", "Jana Kowalskiego"),
            ("siostry Anny Kowalskiej", "Anny Kowalskiej"),
            ("św. Anny Kowalskiej", "Anny Kowalskiej"),
            ("świętej Anny Kowalskiej", "Anny Kowalskiej"),
            ("świętego Jana Kowalskiego", "Jana Kowalskiego"),
            ("im. Jana Kowalskiego", "Jana Kowalskiego"),
            ("imienia Jana Kowalskiego", "Jana Kowalskiego"),
        ]

        comp = NameComparator()

        for i, (lhs, rhs) in enumerate(test_cases):
            with self.subTest(i=i, lhs=lhs, rhs=rhs):
                self.assertTrue(comp.equals(lhs, rhs))
