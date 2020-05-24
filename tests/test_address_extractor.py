import json
import unittest
from collections import Counter
from itertools import chain
from unittest.mock import MagicMock

from data_provider.address_provider import AddressProvider
from env_utils.base_dir import base_dir
from parsers.address_extractor import AddressExtractor


class AddressExtractorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(f'{base_dir}/data/test_data/addresses_from_title_and_description.json', encoding='utf-8') as handle:
            json_obj = json.loads(handle.read())

        cls.all_flats = {int(id): json_obj[id] for id in json_obj}

    def setUp(self):
        self.extractor = AddressExtractor(AddressProvider.Instance())

    def test_case_matters(self):
        status, *_ = self.extractor("Oferuję do wynajęcia śliczne mieszkanie 4-pokojowe") # won't match "Śliczna" street
        self.assertFalse(status)

    def _compare_address_results(self, flat, found_address):
        expected = flat['locations']
        actual = found_address.street + found_address.estate + found_address.district

        expected = set(Counter(expected).keys())
        actual = set(Counter(actual).keys())

        matched = { key: key in actual for key in expected}
        extra_matches = actual.difference(expected)

        return self.assertTrue(expected.issubset(actual),
                               f'\n'
                               + f'[matched from expected] = {matched}\n\n'
                               + f'[extra matches] =\n{extra_matches}\n\n'
                               + f'[title] =\n{flat["title"]}\n\n'
                               + f'[description] =\n {flat["description"]}\n\n')

    def test_regression(self):
        import logging
        logging.root.setLevel(logging.NOTSET)
        passing_tests = [AddressExtractorTest.all_flats[i] for i
                         in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 20, 21, 23, 24, 25, 27]]
        self.assertEqual(len(passing_tests), 21)

        for i, flat in enumerate(passing_tests):
            _, _, found_address = self.extractor(flat['title'] + flat['description'])
            self._compare_address_results(flat, found_address)

    def test_extraction_address_that_contains_only_surname(self):
        *_, found_address = self.extractor("Zamoyskiego")
        self.assertIn("Jana Zamoyskiego", list(chain(found_address.district, found_address.estate, found_address.street)))

    def test_extract_address_with_unit_number(self):
        streets = [{
            "official": "Jana Zamoyskiego",
            "colloquial": [],
        }]

        mocked_address_provider = MagicMock(**{
            'streets': iter(streets),
            'districts': iter([]),
            'estates': iter([]),
        })

        extractor = AddressExtractor(mocked_address_provider)
        *_, found_address = extractor("Zamoyskiego 15")
        self.assertIn("Jana Zamoyskiego 15", found_address.street)
        self.assertTrue(len(found_address.district) == len(found_address.estate) == 0)


if __name__ == "__main__":
    unittest.main()
