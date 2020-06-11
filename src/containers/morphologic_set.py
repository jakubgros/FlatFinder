import functools
from collections import defaultdict

from comparators.morphologic_comparator import MorphologicComparator
from env_utils.config import config
from text.analysis.morphologic_analyser import MorphologicAnalyser, morphologic_analyser


class MorphologicSet:
    """ Container that serves for storing words and easy interrogation it with words in different forms. i.e.
        MorphologicSet that stores word "doktor" satisfies the following condition:
        any((word in morphologic_set) for word in ['doktor', 'doktora', 'doktorów']) == True
    """

    @staticmethod
    def _get_internal_key(elem):
        return elem[0]

    def __init__(self, list_of_words):

        self.analyser = morphologic_analyser

        self.data = defaultdict(set)
        self.comparator = MorphologicComparator()
        # to improve algorithm we assume here that every word no matter of it's form starts with the same letter e.g.
        # "doktor"[0] = "doktora"[0] = "doktorów"[0] = "dr"[0] = "doktorem"[0] and so on...
        # thanks to that we don't need to apply morphologic analysis on each element of the container,
        # only on the elements starting with the same letter
        for elem in list_of_words:
            internal_key = self._get_internal_key(elem)
            self.data[internal_key].add(elem)

    @functools.lru_cache(maxsize=config["cache_size"])
    def __contains__(self, key):
        internal_key = self._get_internal_key(key)
        data = self.data[internal_key]
        for elem in data:
            if self.comparator.equals(elem, key):
                return True

        return False
