from comparators.morphologic_comparator import MorphologicComparator
from text.text_searcher import TextSearcher


class BachelorPadExtractor:
    attribute_name = 'bachelor pad'

    def __call__(self, description: str):
        phrases_to_look_for = ['kawalerka']

        comparator = MorphologicComparator().equals

        for phrase in phrases_to_look_for:
            found, _ = TextSearcher.find(
                phrase_to_find=phrase,
                text=description,
                equality_comparator=comparator)

            if found:
                return {True}

        return {False}
