import json
import traceback
import unittest
from collections import Counter
from itertools import chain

from data_provider.address_provider import address_provider
from env_utils.base_dir import base_dir
from parsers.address_extractor import AddressExtractor
from tests.testing_utilities import MockedAddressProvider
from text.analysis.context_analysers.first_word_of_sentence_context import FirstWordOfSentenceContext
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext

DISABLE_PARALLELIZED_COMPUTATION = False
if DISABLE_PARALLELIZED_COMPUTATION:
    import multiprocess.dummy as mp
else:
    import multiprocess as mp


class AddressExtractorTest(unittest.TestCase):

    def _compare_address_results(self, flat, found_address, *, accept_extra_matches):
        expected = flat['locations']
        actual = [match.location for match in chain(found_address.street, found_address.estate, found_address.district)]

        expected = set(Counter(expected).keys())
        actual = set(Counter(actual).keys())

        matched = {key: key in actual for key in expected}
        extra_matches = actual.difference(expected)

        msg = f'\n' \
              + f'[matched from expected] = {matched}\n\n' \
              + f'[extra matches] =\n{extra_matches if len(extra_matches) > 0 else "NO EXTRA MATCHES"}\n\n' \
              + f'[title] =\n{flat["title"]}\n\n' \
              + f'[description] =\n {flat["description"]}\n\n'

        if accept_extra_matches:
            self.assertTrue(expected.issubset(actual), msg)
        else:
            self.assertTrue(expected == actual, msg)

        self.assertEqual(extra_matches, flat['extra_matches'], "EXTRA MATCHES ARE NOT CORRECT\n"+msg)


    @staticmethod
    def _load_regression_cases():
        with open(f'{base_dir}/data/test_data/addresses_from_title_and_description.json', encoding='utf-8') as handle:
            json_obj = json.loads(handle.read())

        # TODO REMOVE
        for test_case in json_obj.values():
            test_case['extra_matches'] = set()

        json_obj['2']['extra_matches'] = {'Osiedle'}
        json_obj['5']['extra_matches'] = {'Mogilska'}
        json_obj['9']['extra_matches'] = {'Park Bednarskiego', 'Kazimierz'}
        json_obj['11']['extra_matches'] = {'Osiedle', 'Szybka'}
        json_obj['12']['extra_matches'] = {'św. Jana', 'Jana XXIII', 'Izydora Stella-Sawickiego', 'Jana Sawickiego', 'Lotnicza'}
        json_obj['13']['extra_matches'] = {'Osiedle'}
        json_obj['14']['extra_matches'] = {'Bolesława Komorowskiego', 'Krakowska'}
        json_obj['15']['extra_matches'] = {'Bieżanów', 'Nowa'}
        json_obj['16']['extra_matches'] = {'Dworzec', 'Rynek Główny', 'Kazimierz'}
        json_obj['17']['extra_matches'] = {'Osiedle', 'Władysława Łokietka', 'Wrocławska'}
        json_obj['18']['extra_matches'] = {'Osiedle', 'Władysława Łokietka', 'Wrocławska 2'}
        json_obj['19']['extra_matches'] = {'Sołtysowska'}
        json_obj['22']['extra_matches'] = {'Osiedle', 'Władysława Łokietka', 'Wrocławska 2'}
        json_obj['25']['extra_matches'] = {'Dworzec', 'Zakrzówek', 'Czerwone Maki'}
        json_obj['26']['extra_matches'] = {'Mogilska', 'Przy Rondzie', 'Rondo Mogilskie', 'Złota'}
        json_obj['27']['extra_matches'] = {'Seweryna Udzieli', 'Osiedle', 'Krakowska'}
        json_obj['28']['extra_matches'] = {'Kapelanka', 'Rozdroże'}
        # TODO END REMOVE

        disabled_cases = [12, 15, 19, 28]
        test_cases = [value for (key, value) in json_obj.items() if int(key) not in disabled_cases]

        return test_cases

    @staticmethod
    def _get_amount_of_extra_matches(flat, found_address):
        expected = flat['locations']
        actual = [match.location for match in chain(found_address.street, found_address.estate, found_address.district)]

        exp_counter = Counter(expected)
        act_counter = Counter(actual)

        act_counter.subtract(exp_counter)

        extra_matches = 0
        for count in act_counter.values():
            if count > 0:
                extra_matches += count

        return extra_matches

    def test_regression(self):
        import logging
        logging.root.setLevel(logging.NOTSET)

        all_test_cases = self._load_regression_cases()

        extra_matches_count = 0

        def runner(flat):
            try:
                extractor \
                    = AddressExtractor(address_provider, excluded_contexts=[
                    FirstWordOfSentenceContext(),
                    NearbyLocationContext(address_provider=address_provider)
                ])

                _, _, found_address = extractor(flat['title'] + '.\n' + flat['description'])
                return flat, found_address
            except Exception as e:
                trace = traceback.format_exc()
                return None, Exception(str(e) + '\n' + trace)

        with mp.Pool() as pool:
            results = pool.map(runner, all_test_cases)

        for i, (test_case, subtest_result) in enumerate(results):
            with self.subTest(i=i):
                if isinstance(subtest_result, Exception):
                    self.fail(subtest_result)
                else:
                    self._compare_address_results(test_case, subtest_result, accept_extra_matches=True)
                    extra_matches_count += self._get_amount_of_extra_matches(test_case, subtest_result)

        with self.subTest("extra matches"):
            self.assertEqual(65, extra_matches_count)

    def test_case_matters(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Śliczna",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        status, *_ = extractor("Oferuję do wynajęcia śliczne mieszkanie 4-pokojowe")
        self.assertFalse(status)

    def test_case_does_not_matter_phrase_in_text_is_all_upper_case(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Śliczna",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("mieszkanie przy ulicy ŚLICZNEJ")
        self.assertIn("Śliczna", [match.location for match in found_address.street])

    def test_extract_address_with_unit_number(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Jana Zamoyskiego",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("Zamoyskiego 15")
        self.assertIn("Jana Zamoyskiego 15", [match.location for match in found_address.street])

    def test_address_extractor_returns_official_name_if_colloquial_name_matched(self):
        mocked_address_provider = MockedAddressProvider(
            estates=[{
                "official": "Osiedle Na Kozłówce",
                "colloquial": ["Kozłówek"],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("Kozłówek")
        self.assertIn("Osiedle Na Kozłówce", [match.location for match in found_address.estate])

    def test_address_extractor_correctly_compares_names(self):
        streets = [{
            "official": "Tadeusza Kościuszki",
            "colloquial": [],
        }]

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        *_, found_address = extractor("Kościuszki")
        self.assertIn("Tadeusza Kościuszki", [match.location for match in found_address.street])

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        *_, found_address = extractor("Tadeusza Kościuszki")
        self.assertIn("Tadeusza Kościuszki", [match.location for match in found_address.street])

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        *_, found_address = extractor("Tadeusza")
        self.assertNotIn("Tadeusza Kościuszki", [match.location for match in found_address.street])

    def test_address_extractor_performs_morphological_comparison(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Stanisława",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)
        *_, found_address = extractor("Stanisławowi")
        self.assertIn("Stanisława", [match.location for match in found_address.street])

    def test_address_extractor_correctly_recognize_location_type(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Stanisława",
                "colloquial": [],
            }],
            estates=[{
                "official": "Grzegorza",
                "colloquial": [],
            }],
            districts=[{
                "official": "Piotra",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("blah blah Piotra blah Grzegorza blah Stanisława")

        self.assertEqual(len(found_address.street), 1)
        self.assertIn("Stanisława", [match.location for match in found_address.street])

        self.assertEqual(len(found_address.estate), 1)
        self.assertIn("Grzegorza", [match.location for match in found_address.estate])

        self.assertEqual(len(found_address.district), 1)
        self.assertIn("Piotra", [match.location for match in found_address.district])

    def test_Krakow_city_is_not_recognized_as_Kraka_street(self):

        mocked_address_provider = MockedAddressProvider(streets=[{
            "official": "Kraka",
            "colloquial": [],
        }],
        )

        extractor = AddressExtractor(mocked_address_provider)

        has_found, *_ = extractor("miasto Kraków")
        self.assertFalse(has_found)

        has_found, *_ = extractor("w Krakowie")
        self.assertFalse(has_found)

    def test_word_is_not_interpreted_as_location_if_it_is_first_word_of_a_sentence(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Piękna",
                "colloquial": [],
            }],
        )

        extractor = AddressExtractor(mocked_address_provider,
                                     excluded_contexts=[FirstWordOfSentenceContext()])

        has_found, *_ = extractor("Jakieś zdanie. Piękna okolica.")
        self.assertFalse(has_found)

        has_found, *_ = extractor("Jakieś zdanie. Lokalizacja - Piękna 13")
        self.assertTrue(has_found)

    def test_location_is_not_matched_if_it_is_not_flat_address(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Szeroka",
                    "colloquial": [],
                },
                {
                    "official": "Karmelicka",
                    "colloquial": [],
                }
            ],
            places=[{
                "official": "Ikea",
                "colloquial": [],
            }
            ]
        )

        ctx_analyser = NearbyLocationContext(introducers={'w sąsiedztwie'},
                                             conjunctions={'i'},
                                             address_provider=mocked_address_provider)
        extractor = AddressExtractor(mocked_address_provider, excluded_contexts=[ctx_analyser])

        *_, found_address = extractor("Mieszkanie znajduje się na ulicy Karmelickiej. W sąsiedztwie ul. Szeroka i Ikea")
        self.assertIn("Karmelicka", [match.location for match in found_address.street])
        self.assertEqual(1, len(found_address.all_addresses))

    def test_only_longest_location_from_overlapping_matches_is_returned(self):

        with self.subTest():
            mocked_address_provider = MockedAddressProvider(
                streets=[
                    {
                        "official": "Zygmunta Starego",
                        "colloquial": [],
                    },
                    {
                        "official": "Stare Podgórze",
                        "colloquial": [],
                    }
                ],
            )

            extractor = AddressExtractor(mocked_address_provider)
            *_, found_address = extractor(
                "\nDo wynajęcia 1-pokojowe funkcjonalne mieszkanie w spokojnej, dobrze skomunikowanej"
                " okolicy - Stare Podgórze przy ulicy Zamoyskiego, bardzo dobry dojazd do każdej części miasta.")
            names_of_matched_locations = [match.location for match in found_address.all]

            self.assertIn("Stare Podgórze", names_of_matched_locations)
            self.assertNotIn("Zygmunta Starego", names_of_matched_locations)

        with self.subTest():
            mocked_address_provider = MockedAddressProvider(
                streets=[{
                    "official": "Bronowicka",
                    "colloquial": [],
                }],
                places=[{
                    "official": "Galeria Bronowicka",
                    "colloquial": [],
                }]
            )

            extractor = AddressExtractor(mocked_address_provider)
            *_, found_address = extractor("Galeria Bronowicka")
            names_of_matched_locations = [match.location for match in found_address.all]

            self.assertIn("Galeria Bronowicka", names_of_matched_locations)
            self.assertNotIn("Bronowicka", names_of_matched_locations)



    def test_temp(self):  # TODO remove
        import logging
        logging.root.setLevel(logging.NOTSET)

        all_test_cases = self._load_regression_cases()
        flat = all_test_cases[1] #11

        extractor = AddressExtractor(address_provider, excluded_contexts=[
            FirstWordOfSentenceContext(),
            NearbyLocationContext(address_provider=address_provider)
        ])

        *_, found_address = extractor(flat['title'] + '.\n' + flat['description'])
        self._compare_address_results(flat, found_address, accept_extra_matches=False)


if __name__ == "__main__":
    unittest.main()
