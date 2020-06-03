import unittest

from parsers.address_extractor import AddressMatch
from text.analysis.context_analyser import ContextNotFirstWordOfSentence
from utilities.utilities import split_on_special_characters


class TestContextAnalyser(unittest.TestCase):

    def _test_not_first_word_of_sentence_helper(self, sentence, analysis_subject, expected_result):
        source = split_on_special_characters(sentence, preserve_special_characters=True)
        slice_beg = source.index(analysis_subject)
        slice_end = slice_beg + len(split_on_special_characters(analysis_subject, preserve_special_characters=True))
        match = AddressMatch(
            source=source,
            match_slice_position=(slice_beg, slice_end),
            location=''  # doesn't matter
        )
        assert match.matched_phrase == analysis_subject

        self.assertEqual(ContextNotFirstWordOfSentence.does_apply(match), expected_result)

    def test_context_not_first_word_of_sentence(self):
        self._test_not_first_word_of_sentence_helper("Jakieś zdanie. Blisko do centrum.", "Blisko", False)
        self._test_not_first_word_of_sentence_helper("Jakieś zdanie. Blabla Blisko do centrum.", "Blisko", True)

        self._test_not_first_word_of_sentence_helper("Blisko do sklepu", "Blisko", False)
        self._test_not_first_word_of_sentence_helper("Blabla Blisko do sklepu", "Blisko", True)

        self._test_not_first_word_of_sentence_helper("\nBlisko do sklepu", "Blisko", False)
        self._test_not_first_word_of_sentence_helper("\nBlabla Blisko do sklepu", "Blisko", True)
        self._test_not_first_word_of_sentence_helper("Blabla \n Blisko do sklepu", "Blisko", True)

        self._test_not_first_word_of_sentence_helper("Dobra lokizacja.\n Blisko do sklepu", "Blisko", False)
        self._test_not_first_word_of_sentence_helper("Dobra lokizacja.\n Blabla Blisko do sklepu", "Blisko", True)
        self._test_not_first_word_of_sentence_helper("Dobra lokizacja. Blabla \n Blisko do sklepu", "Blisko", True)


if __name__ == '__main__':
    unittest.main()
