from typing import Set

from comparators.morphologic_comparator import MorphologicComparator
from text.text_searcher import TextSearcher


class DescriptionAndTitleFilter:
    def __init__(self, black_list_phrase: Set):
        self.black_list_phrase = black_list_phrase

    def _contains_phrase(self, phrase, flat):
        comparator = MorphologicComparator().equals

        found_in_title, _ = TextSearcher.find(
            phrase_to_find=phrase,
            text=flat.title,
            equality_comparator=comparator)

        if found_in_title:
            return True

        found_in_description, _ = TextSearcher.find(
            phrase_to_find=phrase,
            text=flat.description,
            equality_comparator=comparator)

        if found_in_description:
            return True

        return False

    def __call__(self, flats):

        matching_filter = []

        for flat in flats:
            for phrase in self.black_list_phrase:

                if not self._contains_phrase(phrase, flat):
                    matching_filter.append(flat)

        return matching_filter
