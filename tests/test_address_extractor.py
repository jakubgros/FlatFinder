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
from text.analysis.context_analysers.price_context import PriceContext

DISABLE_PARALLELIZED_COMPUTATION = False
if DISABLE_PARALLELIZED_COMPUTATION:
    import multiprocess.dummy as mp
else:
    import multiprocess as mp


class AddressExtractorTest(unittest.TestCase):

    def _compare_address_results(self, flat, found_address):
        expected = flat['locations']
        actual = [str(match.location) for match in
                  chain(found_address.street, found_address.estate, found_address.district)]

        expected = set(Counter(expected).keys())
        actual = set(Counter(actual).keys())

        matched = {key: key in actual for key in expected}
        extra_matches = actual.difference(expected)

        msg = (f'\n'
               f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
               f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
               f'[description] =\n {flat["description"]}\n\n'
               f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
               f'[matched from expected] = {matched}\n\n'
               f'[extra matches] =\n{extra_matches if len(extra_matches) > 0 else "NO EXTRA MATCHES"}\n\n'
               f'[title] =\n{flat["title"]}\n\n'
               f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
               f'@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')

        if flat.get('ignore_extra_matches', False):
            self.assertTrue(expected.issubset(actual), msg)
        elif 'extra_matches' in flat:
            self.assertTrue(expected.issubset(actual), msg)
            self.assertEqual(extra_matches, flat['extra_matches'], "EXTRA MATCHES ARE NOT CORRECT\n" + msg)
        else:
            self.assertTrue(expected == actual, msg)

    @staticmethod
    def _load_regression_cases():
        with open(f'{base_dir}/data/test_data/addresses_from_title_and_description.json', encoding='utf-8') as handle:
            json_obj = json.loads(handle.read())

        disabled_cases = [12, 15, 19, 26, 33, 40, 50]
        test_cases = [value for (key, value) in json_obj.items() if int(key) not in disabled_cases]

        # TODO REMOVE
        test_cases[9]['extra_matches'] = {'Kazimierz', 'Bednarska'}
        test_cases[11]['extra_matches'] = {'Szybka'}
        test_cases[13]['extra_matches'] = {'Bolesława Komorowskiego', 'Krakowska'}
        test_cases[15]['extra_matches'] = {'Wrocławska'}
        test_cases[16]['extra_matches'] = {'Wrocławska'}
        test_cases[20]['extra_matches'] = {'Zakrzówek', 'Czerwone Maki'}
        test_cases[21]['extra_matches'] = {'Przy Rondzie'}
        test_cases[22]['extra_matches'] = {'Seweryna Udzieli'}
        test_cases[23]['extra_matches'] = {'Armii Krajowej'}
        test_cases[25]['extra_matches'] = {'Błonie', 'Rynek Główny'}
        test_cases[26]['extra_matches'] = {'Wielicka'}
        test_cases[27]['extra_matches'] = {'Błonie', 'gen. Tadeusza Kościuszki'}
        test_cases[28]['extra_matches'] = {'Osiedle'}
        test_cases[29]['extra_matches'] = {'Kazimierz', 'Sukiennicza', 'św. Bronisławy', 'Koletek', 'Rynek Główny', 'Stare Miasto', 'Wawel'}
        test_cases[30]['extra_matches'] = {'Koszykarska', 'Nowohucka', 'Podgórze'}
        test_cases[32]['extra_matches'] = {'Kazimierza Wielkiego', 'Rynek Główny', 'Planty'}
        test_cases[33]['extra_matches'] = {'Podgórze', 'św. Kingi'}
        test_cases[34]['extra_matches'] = {'Saska', 'Rynek Główny', 'Kazimierz'}
        test_cases[35]['extra_matches'] = {'Królewska', 'Stare Miasto', 'Rynek Główny'}
        test_cases[36]['extra_matches'] = {'Stare Miasto', 'Jasna', 'Przyjemna', 'Bartosza', 'Widok', 'Podgórska', 'Kazimierz'}
        test_cases[37]['extra_matches'] = {'Ciepłownicza', 'Sikorki', 'Nowohucka', 'Sołtysowska', 'Nowa Huta'}
        test_cases[38]['extra_matches'] = {'Rynek Główny', 'Dębnicka', 'Błonie'}
        test_cases[40]['extra_matches'] = {'Kazimierza Wielkiego', 'Lublańska', 'Dobrego Pasterza', 'Adama Chmiela', 'Wodna'}
        test_cases[41]['extra_matches'] = {'św. Piotra', 'Rondo Mogilskie'}
        test_cases[43]['extra_matches'] = {'Rynek Główny', 'Nowa', 'Błonie', 'Wawel', 'Krakowska'}
        test_cases[44]['extra_matches'] = {'Wawel', 'Powiśle', 'Zwierzyniecka', 'Rynek Główny', 'Smoleńsk'}
        test_cases[45]['extra_matches'] = {'Podgórze', 'Henryka i Karola Czeczów', 'Mariana Domagały', 'Agatowa'}


        for test_case in test_cases[25:]:
            test_case['ignore_extra_matches'] = True
        # TODO END REMOVE

        return test_cases

    @unittest.skip
    def test_temp(self):  # TODO remove
        import logging
        logging.root.setLevel(logging.NOTSET)

        all_test_cases = self._load_regression_cases()
        flat = all_test_cases[46]
        flat['ignore_extra_matches'] = False

        extractor = AddressExtractor(address_provider, excluded_contexts=[
            FirstWordOfSentenceContext(),
            NearbyLocationContext(address_provider=address_provider)
        ])

        found_address = extractor(flat['title'] + '.\n' + flat['description'])
        self._compare_address_results(flat, found_address)

    @staticmethod
    def _get_amount_of_extra_matches(flat, found_address):
        expected = flat['locations']
        actual = [str(match.location) for match in
                  chain(found_address.street, found_address.estate, found_address.district)]

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
                extractor = AddressExtractor(address_provider, excluded_contexts=[
                    FirstWordOfSentenceContext(),
                    NearbyLocationContext(address_provider=address_provider),
                    PriceContext()
                ])

                found_address = extractor(flat['title'] + '.\n' + flat['description'])
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
                    self._compare_address_results(test_case, subtest_result)
            extra_matches_count += self._get_amount_of_extra_matches(test_case, subtest_result)

        with self.subTest("extra matches"):
            self.assertEqual(92, extra_matches_count)

    def test_case_matters(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Śliczna",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor("Oferuję do wynajęcia śliczne mieszkanie 4-pokojowe")
        self.assertEqual(0, len(found_address.all))

    def test_case_does_not_matter_phrase_in_text_is_all_upper_case(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Śliczna",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor("mieszkanie przy ulicy ŚLICZNEJ")
        self.assertIn("Śliczna", [str(match.location) for match in found_address.street])

    def test_extract_address_with_unit_number(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Jana Zamoyskiego",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor("Zamoyskiego 15")
        self.assertIn("Jana Zamoyskiego 15", [str(match.location) for match in found_address.street])

    def test_address_extractor_returns_official_name_if_colloquial_name_matched(self):
        mocked_address_provider = MockedAddressProvider(
            estates=[{
                "official": "Osiedle Na Kozłówce",
                "colloquial": ["Kozłówek"],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor("Kozłówek")
        self.assertIn("Osiedle Na Kozłówce", [match.location for match in found_address.estate])

    def test_address_extractor_correctly_compares_names(self):
        streets = [{
            "official": "Tadeusza Kościuszki",
            "colloquial": [],
        }]

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        found_address = extractor("Kościuszki")
        self.assertIn("Tadeusza Kościuszki", [str(match.location) for match in found_address.street])

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        found_address = extractor("Tadeusza Kościuszki")
        self.assertIn("Tadeusza Kościuszki", [str(match.location) for match in found_address.street])

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        found_address = extractor("Tadeusza")
        self.assertNotIn("Tadeusza Kościuszki", [str(match.location) for match in found_address.street])

    def test_address_extractor_performs_morphological_comparison(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Stanisława",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)
        found_address = extractor("Stanisławowi")
        self.assertIn("Stanisława", [str(match.location) for match in found_address.street])

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

        found_address = extractor("blah blah Piotra blah Grzegorza blah Stanisława")

        self.assertEqual(len(found_address.street), 1)
        self.assertIn("Stanisława", [str(match.location) for match in found_address.street])

        self.assertEqual(len(found_address.estate), 1)
        self.assertIn("Grzegorza", [str(match.location) for match in found_address.estate])

        self.assertEqual(len(found_address.district), 1)
        self.assertIn("Piotra", [str(match.location) for match in found_address.district])

    def test_Krakow_city_is_not_recognized_as_Kraka_street(self):

        mocked_address_provider = MockedAddressProvider(streets=[{
            "official": "Kraka",
            "colloquial": [],
        }],
        )

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor("miasto Kraków")
        self.assertEqual(0, len(found_address.all))

        found_address = extractor("w Krakowie")
        self.assertEqual(0, len(found_address.all))

    def test_word_is_not_interpreted_as_location_if_it_is_first_word_of_a_sentence(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Piękna",
                "colloquial": [],
            }],
        )

        extractor = AddressExtractor(mocked_address_provider,
                                     excluded_contexts=[FirstWordOfSentenceContext()])

        found_address = extractor("Jakieś zdanie. Piękna okolica.")
        self.assertEqual(0, len(found_address.all))

        found_address = extractor("Jakieś zdanie. Lokalizacja - Piękna 13")
        self.assertNotEqual(0, len(found_address.all))

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

        found_address = extractor("Mieszkanie znajduje się na ulicy Karmelickiej. W sąsiedztwie ul. Szeroka i Ikea")
        self.assertIn("Karmelicka", [str(match.location) for match in found_address.street])
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
            found_address = extractor(
                "\nDo wynajęcia 1-pokojowe funkcjonalne mieszkanie w spokojnej, dobrze skomunikowanej"
                " okolicy - Stare Podgórze przy ulicy Zamoyskiego, bardzo dobry dojazd do każdej części miasta.")
            names_of_matched_locations = [str(match.location) for match in found_address.all]

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
            found_address = extractor("Galeria Bronowicka")
            names_of_matched_locations = [str(match.location) for match in found_address.all]

            self.assertIn("Galeria Bronowicka", names_of_matched_locations)
            self.assertNotIn("Bronowicka", names_of_matched_locations)

    def test_osiedle_street_is_not_matched_to_osiedle_location_prefix(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Osiedle",
                    "colloquial": [],
                },
            ],
        )

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor("Duże osiedle.")
        self.assertNotIn("Osiedle", [match.location for match in found_address.all])

    def test_zl_is_not_matched_to_zlota_street(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Złota",
                    "colloquial": [],
                },
            ],
        )

        extractor = AddressExtractor(mocked_address_provider, excluded_contexts=[PriceContext()])

        found_address = extractor('czynsz najmu : 1600 zł + 553 ZŁ czynsz administracyjny + media .')
        self.assertNotIn("Złota", [match.location for match in found_address.all])

    def test_duplications_are_merged(self):
        mocked_address_provider = MockedAddressProvider(
            districts=[
                {
                    "official": "Nowa Huta",
                    "colloquial": [],
                },
            ],
        )

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor('Dzielnica Nowa Huta. Mieszkanie się na Nowej Hucie')
        self.assertEqual(1, len(found_address.all))

    def test_street_duplications_are_merged(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Mogilska",
                    "colloquial": [],
                },
            ],
        )

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor('Mieszkanie przy ulicy Mogilskiej. Adres Mogilska 66')
        self.assertIn("Mogilska 66", [str(match.location) for match in found_address.all])
        self.assertEqual(1, len(found_address.all))

        found_address = extractor('Mieszkanie przy ulicy Mogilskiej')
        self.assertIn("Mogilska", [str(match.location) for match in found_address.all])
        self.assertEqual(1, len(found_address.all))

    def test_actual_all_uppercase_bug(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[
                {
                    "official": "Czyżyny",
                    "colloquial": [],
                },
            ],
        )

        extractor = AddressExtractor(mocked_address_provider)

        found_address = extractor('CZYŻYNY')
        self.assertIn("Czyżyny", [str(match.location) for match in found_address.all])
        self.assertEqual(1, len(found_address.all))


if __name__ == "__main__":
    unittest.main()
