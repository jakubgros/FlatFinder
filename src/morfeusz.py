import functools
import logging
import re

from src.exception import FFE_InvalidArgument
from src.exception_rule_type import ExceptionRuleType
from src.exception_rules_container import ExceptionRulesContainer
from src.singleton import Singleton
from src.text_frame import TextFrame

@Singleton
class Morfeusz:

    def __init__(self):
        import morfeusz2
        self.morf = morfeusz2.Morfeusz(dict_path=r'..\third parties\morfeusz2-dictionary-polimorf',
                                       dict_name="polimorf")

    @functools.lru_cache(maxsize=None)
    def get_inflection(self, val):
        """ To improve performance of cache, value passed to the function has to be a single word. If you have a sentence
        you have to call the function many times """
        if len(val.split()) > 1:
            raise FFE_InvalidArgument("Passed multi-word argument. The function accepts only single word as argument.")

        inflection = set(base_form for _, _, (_, base_form, *_) in self.morf.analyse(val))
        assert inflection

        return inflection

    @functools.lru_cache(maxsize=None)
    def equals(self, actual, expected, *, exception_rules=None, title_case_sensitive=False):
        if not exception_rules:
            exception_rules = ExceptionRulesContainer.empty()

        actual_split = [word.strip() for word in re.split('(\+|\(|\)| |-|:|;|!|,|\.|\n)', actual)
                           if word and word.strip()]
        expected_split = [word.strip() for word in re.split('(\+|\(|\)| |-|:|;|!|,|\.|\n)', expected)
                           if word and word.strip()]
        actual_amount_of_words = len(actual_split)
        expected_amount_of_words = len(expected_split)
        if actual_amount_of_words != expected_amount_of_words:
            return False

        inflection_actual = [self.get_inflection(word) for word in actual_split]
        inflection_expected = [self.get_inflection(word) for word in expected_split]

        for word_inflection_actual, word_inflection_expected, actual_word, expected_word\
                in zip(inflection_actual, inflection_expected, actual_split, expected_split):

            force_case_insensitivity \
                = exception_rules.does_apply(actual_word, ExceptionRuleType.FORCE_CASE_INSENTIVITIY)

            test_case_sensitivity = not force_case_insensitivity and title_case_sensitive

            if word_inflection_actual.isdisjoint(word_inflection_expected) or \
                    (test_case_sensitivity and actual_word.istitle() != expected_word.istitle()):
                return False
        return True

    def morphological_synthesis(self, word):
        return [elem[0] for elem in self.morf.generate(word)]