import functools
from collections import defaultdict

from morfeusz import Morfeusz


class MorphologicSet:

    def _get_internal_key(self, elem):
        return elem[0]

    def __init__(self, data):
        self.morf = Morfeusz.Instance()

        self.data = defaultdict(set)
        for elem in data:
            internal_key = self._get_internal_key(elem)
            self.data[internal_key].add(elem)

    @functools.lru_cache(maxsize=10000)
    def __contains__(self, key):
        internal_key = self._get_internal_key(key)
        data = self.data[internal_key]
        for elem in data:
            if self.morf.equals(elem, key):
                return True

        return False
