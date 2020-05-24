from comparators.morphologic_comparator import MorphologicComparator


class ComparisonRule:
    def __init__(self, subject, rule_type, *, match_to_lemma=True):
        self.subject = subject
        self.match_to_lemma = match_to_lemma
        self.rule_type = rule_type

    @property
    def _comparator(self):
        if self.match_to_lemma:
            comparator = MorphologicComparator.equals
        else:
            comparator = lambda lhs, rhs: lhs == rhs

        return comparator

    def does_apply(self, subject_to_check):
        return self._comparator(self.subject, subject_to_check)
