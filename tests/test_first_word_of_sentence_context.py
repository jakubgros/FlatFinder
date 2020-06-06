import unittest

from parsers.address_extractor import AddressMatch
from tests.testing_utilities import find_slice
from text.analysis.context_analysers.first_word_of_sentence_context import FirstWordOfSentenceContext
from utilities.utilities import split_on_special_characters


class TestFirstWordOfSentenceContext(unittest.TestCase):

    def _test_first_word_of_sentence_helper(self, sentence, analysis_subject, expected_result):
        source = split_on_special_characters(sentence, preserve_special_characters=True)
        analysis_subject = split_on_special_characters(analysis_subject, preserve_special_characters=True)

        slice_beg = find_slice(source, analysis_subject)
        assert slice_beg is not None

        slice_end = slice_beg + len(analysis_subject)
        match = AddressMatch(
            source=source,
            match_slice_position=(slice_beg, slice_end),
            location=''  # doesn't matter
        )
        assert match.matched_phrase == ' '.join(analysis_subject)

        ctx_analyser = FirstWordOfSentenceContext()
        self.assertEqual(ctx_analyser(match), expected_result)

        negated_ctx_analyser = FirstWordOfSentenceContext(negate=True)
        self.assertEqual(negated_ctx_analyser(match), not expected_result)

    def test_context_first_word_of_sentence(self):
        self._test_first_word_of_sentence_helper("Jakieś zdanie. Blisko do centrum.", "Blisko", True)
        self._test_first_word_of_sentence_helper("Jakieś zdanie. Blabla Blisko do centrum.", "Blisko", False)

        self._test_first_word_of_sentence_helper("Blisko do sklepu", "Blisko", True)
        self._test_first_word_of_sentence_helper("Blabla Blisko do sklepu", "Blisko", False)

        self._test_first_word_of_sentence_helper("\nBlisko do sklepu", "Blisko", True)
        self._test_first_word_of_sentence_helper("\nBlabla Blisko do sklepu", "Blisko", False)
        self._test_first_word_of_sentence_helper("Blabla \n Blisko do sklepu", "Blisko", False)

        self._test_first_word_of_sentence_helper("Dobra lokizacja.\n Blisko do sklepu", "Blisko", True)
        self._test_first_word_of_sentence_helper("Dobra lokizacja.\n Blabla Blisko do sklepu", "Blisko", False)
        self._test_first_word_of_sentence_helper("Dobra lokizacja. Blabla \n Blisko do sklepu", "Blisko", False)

    def test_dot_with_abbreviation(self):
        self._test_first_word_of_sentence_helper("ul. Bajeczna", "Bajeczna", False)
        self._test_first_word_of_sentence_helper("ul. \n Bajeczna", "Bajeczna", False)


if __name__ == '__main__':
    unittest.main()
