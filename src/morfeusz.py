import functools
import logging
import re
from collections import defaultdict

from src.exception import FFE_InvalidArgument
from src.exception_rule_type import ExceptionRuleType
from src.exception_rules_container import ExceptionRulesContainer
from src.singleton import Singleton
from src.text_frame import TextFrame

@Singleton
class Morfeusz:
    """ The library doesn't have any synchronisation mechanisms so it's not safe to use it in multi-threaded environment
    straightaway - see Morfeusz's documentation how to handle it"""

    def __init__(self):
        import morfeusz2
        self.morf = morfeusz2.Morfeusz(dict_path=r'..\third parties\morfeusz2-dictionary-polimorf',
                                       dict_name="polimorf")

        """ flection:
            mianownik (kto? co?)
            dopełniacz (kogo? czego?)
            celownik (komu? czemu?)
            biernik (kogo? co?)
            narzędnik ((z) kim? (z) czym?)
            miejscownik (o kim? o czym?)
            wołacz (o!).
        """
        #  for easier reading the data is provided in inverted form (lemma to list of flection)
        self._word_to_lemma_extension = self._invert_dict({
            "Bonerowska": ("Bonerowska", "Bonerowskiej", "Bonerowskiej", "Bonerowską", "Bonerowską", "Bonerowskiej", "Bonerowsko"),
        })

    def _invert_dict(self, dictionary):
        inv_map = {}
        for key, values in dictionary.items():
            for v in values:
                inv_map.setdefault(v, set()).add(key)
        return inv_map

    @functools.lru_cache(maxsize=10000)
    def get_inflection(self, val):  # TODO it's probably lemma - learn and rename
        """ To improve performance of cache, value passed to the function has to be a single word. If you have a sentence
        you have to call the function many times """
        if len(val.split()) > 1:
            raise FFE_InvalidArgument("Passed multi-word argument. The function accepts only single word as argument.")

        inflection = set(base_form for _, _, (_, base_form, *_) in self.morf.analyse(val))
        assert inflection

        extension = self._word_to_lemma_extension.get(val, set())
        inflection.update(extension)

        return inflection

    @functools.lru_cache(maxsize=10000)
    def _split(self, text):
        text_split = re.split('(\+|\(|\)| |-|:|;|!|,|\.|\n)', text)
        text_split = [word.strip() for word in text_split if word and word.strip()]

        return text_split

    @functools.lru_cache(maxsize=10000)
    def equals(self, expected, actual, *, exception_rules=None, title_case_sensitive=False, ignore_case_sensitivity_if_actual_is_all_upper_case=False):
        expected_split = self._split(expected)
        actual_split = self._split(actual)

        expected_amount_of_words = len(expected_split)
        actual_amount_of_words = len(actual_split)
        if expected_amount_of_words != actual_amount_of_words:
            return False

        inflection_expected = [self.get_inflection(word) for word in expected_split]
        inflection_actual = [self.get_inflection(word) for word in actual_split]

        for word_inflection_actual, word_inflection_expected, actual_word, expected_word\
                in zip(inflection_actual, inflection_expected, actual_split, expected_split):

            force_case_insensitivity \
                = ignore_case_sensitivity_if_actual_is_all_upper_case and actual.isupper()\
                  or exception_rules and exception_rules.does_apply(actual_word, ExceptionRuleType.FORCE_CASE_INSENTIVITIY)

            test_case_sensitivity = not force_case_insensitivity and title_case_sensitive

            if word_inflection_actual.isdisjoint(word_inflection_expected) or \
                    (test_case_sensitivity and actual_word.istitle() != expected_word.istitle()):
                return False
        return True

    def morphological_synthesis(self, word):
        return [elem[0] for elem in self.morf.generate(word)]
