import functools
import re

from comparators.comparison_rules.comparison_rule_type import ComparisonRuleType
from text.analysis.morphologic_analyser import MorphologicAnalyser


class MorphologicComparator:

    @staticmethod
    @functools.lru_cache(maxsize=10000)
    def equals(expected, actual, *, exception_rules=None, title_case_sensitive=False,
               ignore_case_sensitivity_if_actual_is_all_upper_case=False):

        morf_analyser = MorphologicAnalyser.Instance()
        expected_split = MorphologicComparator._split(expected)
        actual_split = MorphologicComparator._split(actual)

        expected_amount_of_words = len(expected_split)
        actual_amount_of_words = len(actual_split)
        if expected_amount_of_words != actual_amount_of_words:
            return False

        inflection_expected = [morf_analyser.get_inflection(word) for word in expected_split]
        inflection_actual = [morf_analyser.get_inflection(word) for word in actual_split]

        for word_inflection_actual, word_inflection_expected, actual_word, expected_word \
                in zip(inflection_actual, inflection_expected, actual_split, expected_split):

            force_case_insensitivity \
                = ignore_case_sensitivity_if_actual_is_all_upper_case and actual.isupper() \
                  or exception_rules and exception_rules.does_apply(actual_word,
                                                                    ComparisonRuleType.FORCE_CASE_INSENSITIVITY)

            test_case_sensitivity = not force_case_insensitivity and title_case_sensitive

            if word_inflection_actual.isdisjoint(word_inflection_expected) or \
                    (test_case_sensitivity and actual_word.istitle() != expected_word.istitle()):
                return False
        return True

    @staticmethod
    @functools.lru_cache(maxsize=10000) # _split is widely used in different classes, extract to improve cache performance
    def _split(text):
        text_split = re.split('(\+|\(|\)| |-|:|;|!|,|\.|\n)', text)
        text_split = [word.strip() for word in text_split if word and word.strip()]

        return text_split