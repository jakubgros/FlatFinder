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
        return ''.join(ch for ch in val if ch.isalnum() or ch.isspace()).strip().lower()

    def compare(self, lhs, rhs):
        lhs = self._consolidate(lhs)
        rhs = self._consolidate(rhs)

        lhs_amount_of_words = len(lhs.split())
        rhs_amount_of_words = len(rhs.split())
        if lhs_amount_of_words != rhs_amount_of_words:
            return False

        inflection_lhs = self.get_inflection(lhs)
        inflection_rhs = self.get_inflection(rhs)

        for word_inflection_lhs, word_inflection_rhs in zip(inflection_lhs, inflection_rhs):
            if word_inflection_lhs.isdisjoint(word_inflection_rhs):
                return False
        return True
