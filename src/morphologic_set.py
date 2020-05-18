import functools

from morfeusz import Morfeusz


class MorphologicSet:
    def __init__(self, data):
        self.data = set(data)
        self.morf = Morfeusz.Instance()

    @functools.lru_cache(maxsize=None)
    def __contains__(self, key):
        for elem in self.data:
            if self.morf.equals(elem, key):
                return True

        return False