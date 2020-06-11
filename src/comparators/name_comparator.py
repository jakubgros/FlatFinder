from itertools import zip_longest

from comparators.morphologic_comparator import MorphologicComparator
from exception.exception import FFE_InvalidArgument
from parsers.human_name_parser import human_name_parser


class NameComparator:
    def __init__(self, ignore_case_sensitivity_if_actual_upper_case=False):
        self.name_parser = human_name_parser
        self.comparator = MorphologicComparator(
            ignore_case_sensitivity_if_actual_upper_case=ignore_case_sensitivity_if_actual_upper_case)

    def _all_equal(self, lhs, rhs):
        return all(self.comparator.equals(*comp_pair) for comp_pair in zip_longest(lhs, rhs, fillvalue=""))

    def equals(self, expected: str, actual: str) -> bool:

        try:
            name_expected = self.name_parser.parse(expected)
            name_actual = self.name_parser.parse(actual)
        except FFE_InvalidArgument:
            return False

        any_name_not_provided = not name_expected.first_name or not name_actual.first_name
        any_surname_provided = name_expected.last_name or name_actual.last_name

        if any_name_not_provided and any_surname_provided:
            return self._all_equal(name_expected.last_name, name_actual.last_name)
        else:
            return self._all_equal(name_expected.first_name, name_actual.first_name) \
                   and self._all_equal(name_expected.last_name, name_actual.last_name)
