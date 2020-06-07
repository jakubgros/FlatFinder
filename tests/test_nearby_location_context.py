import unittest

from containers.address_match import AddressMatch
from tests.testing_utilities import find_slice
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext
from utilities.utilities import split_on_special_characters


class TestNearbyLocationContext(unittest.TestCase):
    def _test_nearby_location_context_helper(self, sentence, analysis_subject, expected_result):
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

        ctx_analyser = NearbyLocationContext()
        self.assertEqual(ctx_analyser(match), expected_result)

        negated_ctx_analyser = NearbyLocationContext(negate=True)
        self.assertEqual(negated_ctx_analyser(match), not expected_result)

    def test_nearby_location_context(self):
        self._test_nearby_location_context_helper(
            "Znakomita lokalizacja w sąsiedztwie Ronda Grunwaldzkiego i Wawelu",
            "Ronda Grunwaldzkiego",
            True)

    def test_nearby_location_context_with_conjunction(self):
        self._test_nearby_location_context_helper(
            "Znakomita lokalizacja w sąsiedztwie Ronda Grunwaldzkiego i Wawelu",
            "Wawelu",
            True)

        "W pobliżu Ikea i Galeria Bronowicka"
        "nieopodal MS AGH , Błonia , 3 minuty do biurowców Galileo , Newton , Edison , za oknem basen AGH ."
        "W bezpośrednim sąsiedztwie Park Bednarskiego i wzgórze Lasoty , niedaleko Bulwary Wiślane i Kazimierz ."


if __name__ == '__main__':
    unittest.main()
