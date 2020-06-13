import functools

from comparators.comparison_rules.comparison_rule_type import ComparisonRuleType
from env_utils.config import config
from text.analysis.morphologic_analyser import MorphologicAnalyser, morphologic_analyser
from utilities.utilities import split_on_special_characters


class MorphologicComparator:
    def __init__(self, *,
                 ignore_case_sensitivity_if_actual_upper_case=False,
                 title_case_sensitive=False,
                 comparison_rules=None):

        self.ignore_case_sensitivity_if_actual_upper_case = ignore_case_sensitivity_if_actual_upper_case
        self.title_case_sensitive = title_case_sensitive
        self.rules = comparison_rules

    def _is_case_sensitive_comparison(self, actual_word, rules):
        force_case_insensitivity = self.ignore_case_sensitivity_if_actual_upper_case and actual_word.isupper() \
                                   or rules and rules.does_apply(actual_word,
                                                                 ComparisonRuleType.FORCE_CASE_INSENSITIVITY)

        return not force_case_insensitivity and self.title_case_sensitive

    @functools.lru_cache(maxsize=config["cache_size"])
    def equals(self, expected, actual):
        expected_split = split_on_special_characters(expected)
        actual_split = split_on_special_characters(actual)

        if len(actual_split) != len(expected_split):
            return False

        analyser = morphologic_analyser
        expected_base_form = [analyser.get_base_form(word) for word in expected_split]
        actual_base_form = [analyser.get_base_form(word) for word in actual_split]

        # TOOD change to filter on len(actual_split) == len(split_on_special_characters(subject)) for subject in self.rules
        if len(actual_split) == 1 and self.rules:
            rules = self.rules.get_filtered(lambda rule: rule.rule_type != ComparisonRuleType.FORCE_CASE_INSENSITIVITY)
        else:
            rules = self.rules

        for actual_word_base, expected_word_base, actual_word_original, expected_word_original \
                in zip(actual_base_form, expected_base_form, actual_split, expected_split):

            test_case_sensitivity = self._is_case_sensitive_comparison(actual_word_original, rules)
            are_not_equal = actual_word_base.isdisjoint(expected_word_base)

            if are_not_equal \
                    or (test_case_sensitivity and actual_word_original.istitle() != expected_word_original.istitle()):
                return False

        return True
