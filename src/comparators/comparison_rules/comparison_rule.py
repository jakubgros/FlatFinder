from comparators.morphologic_comparator import MorphologicComparator
from utilities.utilities import split_on_special_characters


class ComparisonRule:
    def __init__(self, subject, rule_type, *, comparator=MorphologicComparator().equals):
        self.subject = subject
        self.rule_type = rule_type
        self._comparator = comparator

    def does_apply(self, *, subject, context=None):
        if context and len(split_on_special_characters(subject)) >= len(context):
            return False
        else:
            return self._comparator(self.subject, subject)
