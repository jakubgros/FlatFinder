import functools
from collections import defaultdict

from text.analysis.morphologic_analyser import MorphologicAnalyser
from comparators.morphologic_comparator import MorphologicComparator


class MorphologicSet:

    def _get_internal_key(self, elem):
        return elem[0]

    def __init__(self, data):
        self.morf = MorphologicAnalyser.Instance()

        self.data = defaultdict(set)
        for elem in data:
            internal_key = self._get_internal_key(elem)
            self.data[internal_key].add(elem)

    @functools.lru_cache(maxsize=10000)
    def __contains__(self, key):
        internal_key = self._get_internal_key(key)
        data = self.data[internal_key]
        for elem in data:
            if MorphologicComparator().equals(elem, key):
                return True

        return False
