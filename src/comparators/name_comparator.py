from itertools import zip_longest

from comparators.morphologic_comparator import MorphologicComparator
from parsers.human_name_parser import HumanNameParser


class NameComparator:
    @staticmethod
    def equals(expected: str, actual: str, ignore_case_sensitivity_if_actual_is_all_upper_case: bool=False) -> bool:
        name_parser = HumanNameParser.Instance()

        _, expected_first, expected_last = name_parser.parse(expected)
        _, actual_first, actual_last = name_parser.parse(actual)

        comparator = MorphologicComparator(
            ignore_case_sensitivity_if_actual_upper_case=ignore_case_sensitivity_if_actual_is_all_upper_case)


        if (not expected_first or not actual_first) and (actual_first or actual_last):
            return all(comparator.equals(*comp_pair)
                       for comp_pair in zip_longest(expected_last, actual_last, fillvalue=""))
        else:
            return all(comparator.equals(*comp_pair)
                       for comp_pair in zip_longest(expected_first, actual_first, fillvalue="")) \
                   and all(comparator.equals(*comp_pair)
                           for comp_pair in zip_longest(expected_last, actual_last, fillvalue=""))
