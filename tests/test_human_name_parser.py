import unittest
from collections import Counter

from human_name_parser import HumanNameParser


class HumanNameParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = HumanNameParser.Instance()

    def _compare_list(self, actual, expected):
        actual_counter = Counter(actual)
        expect_counter = Counter(expected)

        are_equal = actual_counter == expect_counter
        expect_counter.subtract(actual_counter)
        return are_equal, expect_counter

    def _testParsing(self,
                     to_parse,
                     expected_titles_list=[],
                     expected_given_names_list=[],
                     expected_surnames_list=[]):
        actual_title, actual_given_name, actual_surname = self.parser.parse(to_parse)

        title_are_equal, title_comparison_result = self._compare_list(actual_title, expected_titles_list)
        given_name_are_equal, given_name_comparison_result = self._compare_list(actual_given_name,
                                                                                expected_given_names_list)
        surname_are_equal, surname_comparison_result = self._compare_list(actual_surname, expected_surnames_list)

        error_msg = ""
        if not title_are_equal:
            error_msg += f"title_are_equal={title_are_equal}: \n"
            error_msg += str(title_comparison_result)
            error_msg += "\n"
        if not given_name_are_equal:
            error_msg += f"given_name_are_equal={given_name_are_equal}: \n"
            error_msg += str(given_name_comparison_result)
            error_msg += "\n"
        if not surname_are_equal:
            error_msg += f"surname_are_equal={surname_are_equal}: \n"
            error_msg += str(surname_comparison_result)
            error_msg += "\n"

        if error_msg:
            self.fail(error_msg)

    def test(self):
        all_test_cases = [
            ("Jan Kowalski", [], ["Jan"], ["Kowalski"]),
            ("ks. Jana Kowalskiego", ["ks"], ["Jana"], ["Kowalskiego"]),
            ("księdza Jana Kowalskiego", ["księdza"], ["Jana"], ["Kowalskiego"]),
            ("ks. abp. Jana Zenona Kowalskiego-Nowaka", ["ks", "abp"], ["Jana", "Zenona"], ["Kowalskiego", "Nowaka"]),
            ("Kowalskiego", [], [], ["Kowalskiego"]),
            ("ks. Kowalskiego", ["ks"], [], ["Kowalskiego"]),
            ("ks. Jana", ["ks"], ["Jana"], [])
        ]

        for idx, (name, *result) in enumerate(all_test_cases):
            with self.subTest(i=idx, name=name):
                self._testParsing(name, *result)