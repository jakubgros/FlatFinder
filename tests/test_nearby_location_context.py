import unittest

from containers.address_match import AddressMatch
from tests.testing_utilities import MockedAddressProvider
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext
from utilities.utilities import split_on_special_characters, find_slice_beg


class TestNearbyLocationContext(unittest.TestCase):

    def _test_nearby_location_context_helper(self, *, sentence, subject, expected_result, conjunctions, introducers, address_provider):
        source = split_on_special_characters(sentence, preserve_special_characters=True)
        analysis_subject = split_on_special_characters(subject, preserve_special_characters=True)

        slice_beg = find_slice_beg(source, analysis_subject)
        assert slice_beg is not None

        slice_end = slice_beg + len(analysis_subject)
        match = AddressMatch(
            source=source,
            match_slice_position=(slice_beg, slice_end),
            location=''  # doesn't matter
        )
        assert match.matched_phrase == ' '.join(analysis_subject)

        ctx_analyser = NearbyLocationContext(
            introducers=introducers, conjunctions=conjunctions, address_provider=address_provider)
        self.assertEqual(expected_result, ctx_analyser(match))

        negated_ctx_analyser = NearbyLocationContext(
            introducers=introducers, conjunctions=conjunctions, negate=True, address_provider=address_provider)
        self.assertEqual(not expected_result, negated_ctx_analyser(match))

    def test_nearby_location_context(self):
        introducers = {'w sąsiedztwie'}
        conjunctions = {'i'}

        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Rondo Grunwaldzkie",
                    "colloquial": [],
                },
                {
                    "official": "Wawel",
                    "colloquial": [],
                },
            ])

        self._test_nearby_location_context_helper(
            sentence="Znakomita lokalizacja w sąsiedztwie Ronda Grunwaldzkiego i Wawelu",
            subject="Ronda Grunwaldzkiego",
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="W Krakowie znajduje się Rondo Grunwaldzkie i Wawel",
            subject="Rondo Grunwaldzkie",
            expected_result=False,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

    def test_nearby_location_context_with_conjunction(self):
        introducers = {'w sąsiedztwie'}
        conjunctions = {'i'}

        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Rondo Grunwaldzkie",
                    "colloquial": [],
                },
                {
                    "official": "Wawel",
                    "colloquial": [],
                },
                {
                    "official": "Karmelicka",
                    "colloquial": [],
                },
            ])

        self._test_nearby_location_context_helper(
            sentence="Znakomita lokalizacja w sąsiedztwie Ronda Grunwaldzkiego i Wawelu",
            subject="Wawelu",
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="W Krakowie znajduje się Rondo Grunwaldzkie i Wawel",
            subject="Wawel",
            expected_result=False,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="Mieszkanie w sąsiedztwie Wawelu. Ulica Karmelicka.",
            subject="Karmelicka",
            expected_result=False,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

    def test_conjuncted_multiple_locations(self):
        introducers = {'w sąsiedztwie'}
        conjunctions = {','}

        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Rondo Grunwaldzkie",
                    "colloquial": [],
                },
                {
                    "official": "Wawel",
                    "colloquial": [],
                },
                {
                    "official": "Karmelicka",
                    "colloquial": [],
                },
            ])

        self._test_nearby_location_context_helper(
            sentence="Znakomita lokalizacja w sąsiedztwie Ronda Grunwaldzkiego, Wawelu, Karmelickiej",
            subject="Wawelu",
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="Znakomita lokalizacja w sąsiedztwie Ronda Grunwaldzkiego, Wawelu, Karmelickiej",
            subject="Karmelickiej",
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="W Krakowie znajduje się Rondo Grunwaldzkie i Wawel",
            subject="Wawel",
            expected_result=False,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

    def test_multiple_consecutive_contexts(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Rondo Grunwaldzkie",
                    "colloquial": [],
                },
                {
                    "official": "Wawel",
                    "colloquial": [],
                },
                {
                    "official": "Stare Miasto",
                    "colloquial": [],
                },
                {
                    "official": "Nowa Huta",
                    "colloquial": [],
                },
            ])

        for subject in ["Rondo Grunwaldzkie", "Wawel", "Stare Miasto", "Nowa Huta"]:
            with self.subTest(subject=subject):
                self._test_nearby_location_context_helper(
                    sentence="W pobliżu Rondo Grunwaldzkie i Wawel. Niedaleko Stare Miasto i Nowa Huta",
                    subject=subject,
                    expected_result=True,
                    introducers={"W pobliżu", "Niedaleko"},
                    conjunctions={'i'},
                    address_provider=mocked_address_provider)

    def test_introducers_are_case_insensitive(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Wawel",
                    "colloquial": [],
                },
            ])

        self._test_nearby_location_context_helper(
            sentence="W pobliżu Wawel.",
            subject="Wawel",
            expected_result=True,
            introducers={"w pobliżu"},
            conjunctions={},
            address_provider=mocked_address_provider)

    def test_conjunction_with_not_address_location(self):
        #  tests the following case: nearby_location_introducer + non_address_location + conjunction + address

        introducers = {"w pobliżu"}
        conjunctions = {"i"}

        mocked_address_provider = MockedAddressProvider(
            streets=[{
                    "official": "Wawel",
                    "colloquial": [],
            }],
            places=[
                {
                    "official": "Ikea",
                    "colloquial": [],
                },
                {
                    "official": "Galeria Bronowicka",
                    "colloquial": [],
                },
            ]
            )

        with self.subTest():
            self._test_nearby_location_context_helper(
                sentence="W pobliżu Ikea i Wawel",
                subject="Wawel",
                expected_result=True,
                introducers=introducers,
                conjunctions=conjunctions,
                address_provider=mocked_address_provider)

        with self.subTest():
            self._test_nearby_location_context_helper(
                sentence="W pobliżu Galeria Bronowicka i Bronowice",
                subject="Bronowice",
                expected_result=True,
                introducers=introducers,
                conjunctions=conjunctions,
                address_provider=mocked_address_provider)

        """ TODO:
            - update default list of introducers and conjunctions to contain all needed values
            - integrate context to regression
            - profile if significant speed decrease
        """
if __name__ == '__main__':
    unittest.main()
