from comparators.morphologic_comparator import MorphologicComparator


class ComparisonRule:
    def __init__(self, subject, rule_type, *, comparator=MorphologicComparator.equals):
        self.subject = subject
        self.rule_type = rule_type
        self._comparator = comparator

    def does_apply(self, val):
        return self._comparator(self.subject, val)
