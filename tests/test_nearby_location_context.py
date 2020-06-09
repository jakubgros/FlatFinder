import unittest

from containers.address_match import AddressMatch
from tests.testing_utilities import MockedAddressProvider
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext
from utilities.utilities import split_on_special_characters, find_slice_beg


class TestNearbyLocationContext(unittest.TestCase):

    def _test_nearby_location_context_helper(self, *, sentence, subject_slice_beg_end, expected_result, conjunctions,
                                             location_type_prefixes={}, introducers, address_provider):
        with self.subTest(sentence=sentence, subject=subject_slice_beg_end, expected_result=expected_result):
            source = split_on_special_characters(sentence, preserve_special_characters=True)

            match = AddressMatch(
                source=source,
                match_slice_position=subject_slice_beg_end,
                location=''  # doesn't matter
            )

            ctx_analyser = NearbyLocationContext(
                introducers=introducers,
                conjunctions=conjunctions,
                address_provider=address_provider,
                location_type_prefixes=location_type_prefixes)
            self.assertEqual(expected_result, ctx_analyser(match))

            negated_ctx_analyser = NearbyLocationContext(
                negate=True,
                introducers=introducers,
                conjunctions=conjunctions,
                address_provider=address_provider,
                location_type_prefixes=location_type_prefixes)
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
            subject_slice_beg_end=(4, 6),  # Ronda Grunwaldzkiego
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="W Krakowie znajduje się Rondo Grunwaldzkie i Wawel",
            subject_slice_beg_end=(4, 6),  # Rondo Grunwaldzkie
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
            subject_slice_beg_end=(7, 8),  # Wawelu
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="W Krakowie znajduje się Rondo Grunwaldzkie i Wawel",
            subject_slice_beg_end=(7, 8),  # "Wawel",
            expected_result=False,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="Mieszkanie w sąsiedztwie Wawelu. Ulica Karmelicka.",
            subject_slice_beg_end=(6, 7),  # Karmelicka
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
            subject_slice_beg_end=(7, 8),  # Wawelu
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="Znakomita lokalizacja w sąsiedztwie Ronda Grunwaldzkiego, Wawelu, Karmelickiej",
            subject_slice_beg_end=(9, 10),  # Karmelickiej
            expected_result=True,
            introducers=introducers,
            conjunctions=conjunctions,
            address_provider=mocked_address_provider)

        self._test_nearby_location_context_helper(
            sentence="W Krakowie znajduje się Rondo Grunwaldzkie i Wawel",
            subject_slice_beg_end=(7, 8),  # Wawel
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

        for subject in [
            (2, 4),  # "Rondo Grunwaldzkie"
            (5, 6),  # "Wawel"
            (8, 10),  # "Stare Miasto"
            (11, 13),  # "Nowa Huta"
        ]:
            with self.subTest(subject=subject):
                self._test_nearby_location_context_helper(
                    sentence="W pobliżu Rondo Grunwaldzkie i Wawel. Niedaleko Stare Miasto i Nowa Huta",
                    subject_slice_beg_end=subject,
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
            subject_slice_beg_end=(2, 3), # "Wawel"
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
                subject_slice_beg_end=(4, 5), # "Wawel"
                expected_result=True,
                introducers=introducers,
                conjunctions=conjunctions,
                address_provider=mocked_address_provider)

        with self.subTest():
            self._test_nearby_location_context_helper(
                sentence="W pobliżu Galeria Bronowicka i Bronowice",
                subject_slice_beg_end=(5, 6), #"Bronowice",
                expected_result=True,
                introducers=introducers,
                conjunctions=conjunctions,
                address_provider=mocked_address_provider)

    def test_conjunction_with_address_having_prefix(self):

        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Szeroka",
                "colloquial": [],
            }],
            places=[{
                "official": "Ikea",
                "colloquial": [],
            }]
        )

        for test_case in [
            ("W pobliżu Ikea i ul. Szeroka", (6, 7)),  # 'Szeroka'
            ("W pobliżu Ikea i ul. Szeroka", (4, 7)),  # 'ul. Szeroka'
            ("W pobliżu Ikea i ul. Szeroka", (2, 3)),  # 'Ikea'

            ("W pobliżu ul. Szeroka i Ikea", (4, 5)), # 'Szeroka'
            ("W pobliżu ul. Szeroka i Ikea", (2, 5)),  # 'ul. Szeroka'
            ("W pobliżu ul. Szeroka i Ikea", (6, 7)), # 'Ikea'
         ]:
            sentence, subject = test_case
            self._test_nearby_location_context_helper(
                sentence=sentence,
                subject_slice_beg_end=subject,
                expected_result=True,
                introducers={"w pobliżu"},
                conjunctions={"i"},
                address_provider=mocked_address_provider)

        """ TODO:
            - update default list of introducers and conjunctions to contain all needed values
            - integrate context to regression
            - profile if significant speed decrease
        """


if __name__ == '__main__':
    unittest.main()
