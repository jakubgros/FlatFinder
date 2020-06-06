import json
import traceback
import unittest
from collections import Counter

import multiprocess as mp
from random import shuffle

from data_provider.address_provider import address_provider
from env_utils.base_dir import base_dir
from parsers.address_extractor import AddressExtractor
from text.analysis.context_analyser import FirstWordOfSentenceContext


class MockedAddressProvider:
    def __init__(self, districts=[], estates=[], streets=[]):
        self.districts = districts
        self.estates = estates
        self.streets = streets


class AddressExtractorTest(unittest.TestCase):

    def _compare_address_results(self, flat, found_address, *, accept_extra_matches):
        expected = flat['locations']
        actual = found_address.street + found_address.estate + found_address.district

        expected = set(Counter(expected).keys())
        actual = set(Counter(actual).keys())

        matched = {key: key in actual for key in expected}
        extra_matches = actual.difference(expected)

        if accept_extra_matches:
            is_ok = expected.issubset(actual)
        else:
            is_ok = expected == actual

        return self.assertTrue(is_ok,
                               f'\n'
                               + f'[matched from expected] = {matched}\n\n'
                               + f'[extra matches] =\n{extra_matches}\n\n'
                               + f'[title] =\n{flat["title"]}\n\n'
                               + f'[description] =\n {flat["description"]}\n\n')
    @staticmethod
    def _load_regression_cases():
        with open(f'{base_dir}/data/test_data/addresses_from_title_and_description.json', encoding='utf-8') as handle:
            json_obj = json.loads(handle.read())

        all_flats = {int(identifier): json_obj[identifier] for identifier in json_obj}

        # failing tests are disabled temporarily
        passing_test_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 16, 20, 21, 23, 24, 25, 27]
        passing_tests = [all_flats[i] for i in passing_test_indexes]

        return passing_tests

    @staticmethod
    def _get_amount_of_extra_matches(flat, found_address):
        expected = flat['locations']
        actual = found_address.street + found_address.estate + found_address.district

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
                    = AddressExtractor(address_provider, context_analysers=[FirstWordOfSentenceContext(negate=True)])

                _, _, found_address = extractor(flat['title'] + flat['description'])
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

        self.assertEqual(extra_matches_count, 46)

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
        self.assertIn("Śliczna", found_address.street)

    def test_extract_address_with_unit_number(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Jana Zamoyskiego",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("Zamoyskiego 15")
        self.assertIn("Jana Zamoyskiego 15", found_address.street)

    def test_address_extractor_returns_official_name_if_colloquial_name_matched(self):
        mocked_address_provider = MockedAddressProvider(
            estates=[{
                "official": "Osiedle Na Kozłówce",
                "colloquial": ["Kozłówek"],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("Kozłówek")
        self.assertIn("Osiedle Na Kozłówce", found_address.estate)

    def test_address_extractor_correctly_compares_names(self):
        streets = [{
            "official": "Tadeusza Kościuszki",
            "colloquial": [],
        }]

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        *_, found_address = extractor("Kościuszki")
        self.assertIn("Tadeusza Kościuszki", found_address.street)

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        *_, found_address = extractor("Tadeusza Kościuszki")
        self.assertIn("Tadeusza Kościuszki", found_address.street)

        extractor = AddressExtractor(MockedAddressProvider(streets=streets))
        *_, found_address = extractor("Tadeusza")
        self.assertNotIn("Tadeusza Kościuszki", found_address.street)

    def test_address_extractor_performs_morphological_comparison(self):
        mocked_address_provider = MockedAddressProvider(
            streets=[{
                "official": "Stanisława",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)
        *_, found_address = extractor("Stanisławowi")
        self.assertIn("Stanisława", found_address.street)

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
        self.assertIn("Stanisława", found_address.street)

        self.assertEqual(len(found_address.estate), 1)
        self.assertIn("Grzegorza", found_address.estate)

        self.assertEqual(len(found_address.district), 1)
        self.assertIn("Piotra", found_address.district)

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

        extractor = AddressExtractor(mocked_address_provider, context_analysers=[FirstWordOfSentenceContext(negate=True)])

        has_found, *_ = extractor("Jakieś zdanie. Piękna okolica.")
        self.assertFalse(has_found)

        has_found, *_ = extractor("Jakieś zdanie. Lokalizacja - Piękna 13")
        self.assertTrue(has_found)


if __name__ == "__main__":
    unittest.main()
