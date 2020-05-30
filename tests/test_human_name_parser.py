import unittest
from collections import Counter

from parsers.human_name_parser import HumanNameParser


class HumanNameParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = HumanNameParser.Instance()

    @staticmethod
    def _compare_lists(actual, expected):
        actual_counter = Counter(actual)
        expect_counter = Counter(expected)

        are_equal = actual_counter == expect_counter
        expect_counter.subtract(actual_counter)
        return are_equal, expect_counter

    def _test_results(self,
                      to_parse,
                      expected_titles_list=[],
                      expected_given_names_list=[],
                      expected_surnames_list=[]):
        actual_title, actual_given_name, actual_surname = self.parser.parse(to_parse)

        title_are_equal, title_comparison_result = self._compare_lists(actual_title, expected_titles_list)
        given_name_are_equal, given_name_comparison_result = self._compare_lists(actual_given_name,
                                                                                 expected_given_names_list)
        surname_are_equal, surname_comparison_result = self._compare_lists(actual_surname, expected_surnames_list)

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

    def test_human_name_parsing(self):
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
                self._test_results(name, *result)

    def test_dots_after_titles_are_ignored(self):
        self.assertEqual(self.parser.parse("inż Jan Kowalski"), self.parser.parse("inż. Jan Kowalski"))

    def test_number_epithets_are_parsed_correctly(self):
        a = self.parser.parse("Mieszko I")
        self.parser.parse("I")
        self.parser.parse("Jan Paweł II")
        self.parser.parse("Jan Paweł XI")
        self.parser.parse("Jan Paweł IV")



