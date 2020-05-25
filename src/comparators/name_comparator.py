from itertools import zip_longest

from comparators.morphologic_comparator import MorphologicComparator
from parsers.human_name_parser import HumanNameParser


class NameComparator:
    def __init__(self, ignore_case_sensitivity_if_actual_upper_case=False):
        self.name_parser = HumanNameParser.Instance()
        self.comparator = MorphologicComparator(
            ignore_case_sensitivity_if_actual_upper_case=ignore_case_sensitivity_if_actual_upper_case)

    def _all_equal(self, lhs, rhs):
        return all(self.comparator.equals(*comp_pair) for comp_pair in zip_longest(lhs, rhs, fillvalue=""))

    def equals(self, expected: str, actual: str) -> bool:

        _, expected_first, expected_last = self.name_parser.parse(expected)
        _, actual_first, actual_last = self.name_parser.parse(actual)

        any_name_not_provided = not expected_first or not actual_first
        any_surname_provided = expected_last or actual_last

        if any_name_not_provided and any_surname_provided:
            return self._all_equal(expected_last, actual_last)
        else:
            return self._all_equal(expected_first, actual_first) and self._all_equal(expected_last, actual_last)
