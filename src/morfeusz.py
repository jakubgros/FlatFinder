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

    def get_inflection(self, val):
        inflection = list()
        for idx, _, (_, base_form, *_) in self.morf.analyse(val):
            if len(inflection) <= idx:
                inflection.append(set())
            inflection[-1].add(base_form)

        return inflection

    def _consolidate(self, val):
        return ''.join(ch for ch in val if ch.isalnum() or ch.isspace()).strip()

    def equals(self, actual, expected, *, exception_rules=None, title_case_sensitive=False):
        if not exception_rules:
            exception_rules = ExceptionRulesContainer.empty()

        actual = self._consolidate(actual)
        expected = self._consolidate(expected)

        actual_amount_of_words = len(actual.split())
        expected_amount_of_words = len(expected.split())
        if actual_amount_of_words != expected_amount_of_words:
            return False

        inflection_actual = self.get_inflection(actual)
        inflection_expected = self.get_inflection(expected)

        for word_inflection_actual, word_inflection_expected, actual_word, expected_word\
                in zip(inflection_actual, inflection_expected, actual.split(), expected.split()):

            force_case_insensitivity \
                = exception_rules.does_apply(actual_word, ExceptionRuleType.FORCE_CASE_INSENTIVITIY)

            test_case_sensitivity = not force_case_insensitivity and title_case_sensitive

            if word_inflection_actual.isdisjoint(word_inflection_expected) or \
                    (test_case_sensitivity and actual_word.istitle() != expected_word.istitle()):
                return False
        return True

    def contains(self, phrase, text, *, exception_rules=None, title_case_sensitive=False):
        frame_size = len(phrase.split())

        for frame in TextFrame(text, frame_size):
            if self.equals(phrase, frame, exception_rules=exception_rules, title_case_sensitive=title_case_sensitive):
                return True

        return False
