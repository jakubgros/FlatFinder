import unittest

from src.name_comparator import NameComparator


class NameComparatorTest(unittest.TestCase):

    def setUp(self):
        self.comp = NameComparator()

    def _test_all_cases(self, test_cases):
        for i, (lhs, rhs) in enumerate(test_cases):
            with self.subTest(i=i, lhs=lhs, rhs=rhs):
                self.assertTrue(self.comp.equals(lhs, rhs))

    def testTitleIgnoringComparisonOfFirstNameAndSurname(self):
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

        self._test_all_cases(test_cases)


    def testTitleIgnoringComparisonOfFirstNameOnly(self):
        test_cases = [
            ("świętej Anny", "Anny"),
            ("ojca Jana", "Jana"),
            ("dr Jana", "Jana"),
            ("prof. Jana", "Jana"),
        ]

        self._test_all_cases(test_cases)

    def testTitleIgnoringComparisonOfSurnameOnly(self):
        test_cases = [
            ("majora Kowalskiego", "Kowalskiego"),
            ("gen. Kowalskiego", "Kowalskiego"),
            ("marszałka Kowalskiego", "Kowalskiego"),
            ("płk. Kowalskiego", "Kowalskiego"),
        ]

        self._test_all_cases(test_cases)

    def testComparisonBetweenLongAndAbbreviatedFormOfTitle(self):
        test_cases = [
            ("ks. Jana Kowalskiego", "księdza Jana Kowalskiego"),
            ("abp. Jana Kowalskiego", "arcybiskupa Jana Kowalskiego"),
            ("gen. Jana Kowalskiego", "generała Jana Kowalskiego"),
            ("gen. Anny Kowalskiej", "generał Anny Kowalskiej"),
            ("marsz. Jana Kowalskiego", " marszałka Jana Kowalskiego"),
            ("marsz. Anny Kowalskiej", "marszałek Anny Kowalskiej"),
            ("płk. Jana Kowalskiego", "pułkownika Jana Kowalskiego"),
            ("płk. Anny Kowalskiej", "pułkownik Anny Kowalskiej"),
            ("bł. Jana Kowalskiego", "błogosławionego Jana Kowalskiego"),
            ("bł. Anny Kowalskiej", "błogosławionej Anny Kowalskiej"),
            ("bp. Jana Kowalskiego", "biskupa Jana Kowalskiego"),
            ("bpa Jana Kowalskiego", "biskupa Jana Kowalskiego"),
            ("bp. Jana Kowalskiego", "bpa Jana Kowalskiego"),
            ("dr Jana Kowalskiego", "doktora Jana Kowalskiego"),
            ("dr Anny Kowalskiej", "doktor Anny Kowalskiej"),
            ("pil. Jana Kowalskiego", "pilota Jana Kowalskiego"),
            ("harc. Jana Kowalskiego", "harcmistrza Jana Kowalskiego"),
            ("Jana Kowalskiego", "profesora Jana Kowalskiego"),
            ("prof. Anny Kowalskiej", "profesor Anny Kowalskiej"),
            ("kmr. Jana Kowalskiego", "komandora Jana Kowalskiego"),
            ("kard. Jana Kowalskiego", "kardynała Jana Kowalskiego"),
            ("mjr. Jana Kowalskiego", "majora Jana Kowalskiego"),
            ("o. Jana Kowalskiego", "ojca Jana Kowalskiego"),
            ("por. Jana Kowalskiego", "porucznika Jana Kowalskiego"),
            ("rtm. Jana Kowalskiego", "rotmistrza Jana Kowalskiego"),
            ("s. Anny Kowalskiej", "siostry Anny Kowalskiej"),
            ("św. Anny Kowalskiej", "świętej Anny Kowalskiej"),
            ("św. Jana Kowalskiego", "świętego Jana Kowalskiego"),
            ("im. Jana Kowalskiego", "imienia Jana Kowalskiego"),
        ]

        self._test_all_cases(test_cases)

    def testComparisonWhenAllTitlesProvidedVsOnlyPartOfTitlesProvided(self):
        test_cases = [
            ("ks. abp. Jana Kowalskiego", "ks. Jana Kowalskiego"),
            ("ks. abp. Jana Kowalskiego", "abp. Jana Kowalskiego"),
            ("ks. abp. Jana Kowalskiego", " Jana Kowalskiego"),
        ]

        self._test_all_cases(test_cases)

    def testComparisonTitlesProvidedInDifferentOrder(self):
        test_cases = [
            ("ks. abp. Jana Kowalskiego", "abp. ks. Jana Kowalskiego"),
        ]

        self._test_all_cases(test_cases)