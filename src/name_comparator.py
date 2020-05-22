from itertools import zip_longest

from Tagger import Tagger
from human_name_parser import HumanNameParser
from singleton import Singleton

from src.morfeusz import Morfeusz

class NameComparator:
    @staticmethod
    def equals(expected: str, actual: str, ignore_case_sensitivity_if_actual_is_all_upper_case: bool=False) -> bool:
        name_parser = HumanNameParser.Instance()

        _, expected_first, expected_last = name_parser.parse(expected)
        _, actual_first, actual_last = name_parser.parse(actual)

        morf = Morfeusz.Instance()

        if (not expected_first or not actual_first) and (actual_first or actual_last):
            return all(morf.equals(*comp_pair, ignore_case_sensitivity_if_actual_is_all_upper_case=ignore_case_sensitivity_if_actual_is_all_upper_case)
                       for comp_pair in zip_longest(expected_last, actual_last, fillvalue=""))
        else:
            return all(morf.equals(*comp_pair, ignore_case_sensitivity_if_actual_is_all_upper_case=ignore_case_sensitivity_if_actual_is_all_upper_case)
                       for comp_pair in zip_longest(expected_first, actual_first, fillvalue="")) \
                   and all(morf.equals(*comp_pair, ignore_case_sensitivity_if_actual_is_all_upper_case=ignore_case_sensitivity_if_actual_is_all_upper_case)
                           for comp_pair in zip_longest(expected_last, actual_last, fillvalue=""))
