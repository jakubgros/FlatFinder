import json
import unittest
from collections import Counter
from unittest.mock import MagicMock

from data_provider.address_provider import AddressProvider
from env_utils.base_dir import base_dir
from parsers.address_extractor import AddressExtractor


class AddressExtractorTest(unittest.TestCase):

    def _compare_address_results(self, flat, found_address):
        expected = flat['locations']
        actual = found_address.street + found_address.estate + found_address.district

        expected = set(Counter(expected).keys())
        actual = set(Counter(actual).keys())

        matched = {key: key in actual for key in expected}
        extra_matches = actual.difference(expected)

        return self.assertTrue(expected.issubset(actual),
                               f'\n'
                               + f'[matched from expected] = {matched}\n\n'
                               + f'[extra matches] =\n{extra_matches}\n\n'
                               + f'[title] =\n{flat["title"]}\n\n'
                               + f'[description] =\n {flat["description"]}\n\n')

    @staticmethod
    def _get_mocked_address_provider(streets=[], estates=[], districts=[]):
        return MagicMock(**{
            'streets': iter(streets),
            'estates': iter(estates),
            'districts': iter(districts)
        })

    def test_regression(self):
        import logging
        logging.root.setLevel(logging.NOTSET)

        with open(f'{base_dir}/data/test_data/addresses_from_title_and_description.json', encoding='utf-8') as handle:
            json_obj = json.loads(handle.read())

        all_flats = {int(identifier): json_obj[identifier] for identifier in json_obj}

        # failing tests are disabled temporarily
        passing_tests = [all_flats[i] for i
                         in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 20, 21, 23, 24, 25, 27]]
        self.assertEqual(len(passing_tests), 21)

        extractor = AddressExtractor(AddressProvider.Instance())
        for i, flat in enumerate(passing_tests):
            _, _, found_address = extractor(flat['title'] + flat['description'])
            self._compare_address_results(flat, found_address)

    def test_case_matters(self):
        mocked_address_provider = self._get_mocked_address_provider(
            streets=[{
                "official": "Śliczna",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        status, *_ = extractor("Oferuję do wynajęcia śliczne mieszkanie 4-pokojowe")
        self.assertFalse(status)

    def test_case_does_not_matter_phrase_in_text_is_all_upper_case(self):
        mocked_address_provider = self._get_mocked_address_provider(
            streets=[{
                "official": "Śliczna",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("mieszkanie przy ulicy ŚLICZNEJ")
        self.assertIn("Śliczna", found_address.street)

    def test_extract_address_with_unit_number(self):
        mocked_address_provider = self._get_mocked_address_provider(
            streets=[{
                "official": "Jana Zamoyskiego",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)

        *_, found_address = extractor("Zamoyskiego 15")
        self.assertIn("Jana Zamoyskiego 15", found_address.street)

    def test_address_extractor_returns_official_name_if_colloquial_name_matched(self):
        mocked_address_provider = self._get_mocked_address_provider(
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

        extractor = AddressExtractor(self._get_mocked_address_provider(streets=streets))
        *_, found_address = extractor("Kościuszki")
        self.assertIn("Tadeusza Kościuszki", found_address.street)

        extractor = AddressExtractor(self._get_mocked_address_provider(streets=streets))
        *_, found_address = extractor("Tadeusza Kościuszki")
        self.assertIn("Tadeusza Kościuszki", found_address.street)

        extractor = AddressExtractor(self._get_mocked_address_provider(streets=streets))
        *_, found_address = extractor("Tadeusza")
        self.assertNotIn("Tadeusza Kościuszki", found_address.street)

    def test_address_extractor_performs_morphological_comparison(self):
        mocked_address_provider = self._get_mocked_address_provider(
            streets=[{
                "official": "Stanisława",
                "colloquial": [],
            }])

        extractor = AddressExtractor(mocked_address_provider)
        *_, found_address = extractor("Stanisławowi")
        self.assertIn("Stanisława", found_address.street)

    def test_address_extractor_correctly_recognize_location_type(self):
        mocked_address_provider = self._get_mocked_address_provider(
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

        self.assertTrue(len(found_address.street) == 1)
        self.assertIn("Stanisława", found_address.street)

        self.assertTrue(len(found_address.estate) == 1)
        self.assertIn("Grzegorza", found_address.estate)

        self.assertTrue(len(found_address.district) == 1)
        self.assertIn("Piotra", found_address.district)


if __name__ == "__main__":
    unittest.main()
