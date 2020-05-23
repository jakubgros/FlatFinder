import unittest
from collections import Counter
from itertools import chain

from src.address_provider import AddressProvider
from src.extractor import AddressExtractor

import xml.etree.ElementTree as ET


class AddressExtractorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tree = ET.parse('../data/tagged/addresses_from_title_and_description/addresses_from_title_and_description.xml')

        root = tree.getroot()

        cls.all_flats = []
        for flatXml in root:
            title = flatXml.find('title').text
            url = flatXml.find('url').text
            description = flatXml.find('description').text
            locations_node = flatXml.find('locations')
            locations = [location.text for location in locations_node]
            cls.all_flats.append({'title': title,
                                  'url': url,
                                  'locations': locations,
                                  'description': description,
                                  })

    def setUp(self):
        self.extractor = AddressExtractor(AddressProvider.Instance("Kraków"))

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

    # TODO remove once all tests in test_bulk passes
    def test_regression(self): #TODO once all passes in testBulk, change compareAddressResult to more strict comparison
        import logging
        logging.root.setLevel(logging.NOTSET)
        passing_tests = [AddressExtractorTest.all_flats[i] for i
                         in [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 16, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                             32, 33, 34, 36, 37, 39, 43, 44, 45, 46, 48, 50]]
        self.assertEqual(len(passing_tests), 37)

        for i, flat in enumerate(passing_tests):
            _, _, found_address = self.extractor(flat['title'] + flat['description'])
            self._compare_address_results(flat, found_address)

    def test_bulk(self):
        import logging
        logging.root.setLevel(logging.NOTSET)

        for i, flat in enumerate(AddressExtractorTest.all_flats):
            with self.subTest(i=i):
                _, _, found_address = self.extractor(flat['title'] + flat['description'])
                self._compare_address_results(flat, found_address)

    def test_not_passing(self): #TODO remove once all tests in test_bulk passes
        passing_tests = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 16, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                             32, 33, 34, 36, 37, 39, 43, 44, 45, 46, 48, 50]
        self.assertEqual(len(passing_tests), 37)

        for i, flat in enumerate(AddressExtractorTest.all_flats):
            if i not in passing_tests:
                with self.subTest(i=i):
                    _, _, found_address = self.extractor(flat['title'] + flat['description'])
                    self._compare_address_results(flat, found_address)


    def test_extraction_address_that_contains_only_surname(self):
        *_, found_address = self.extractor("Zamoyskiego")
        self.assertIn("Jana Zamoyskiego", chain(found_address.district, found_address.estate, found_address.street))

if __name__ == "__main__":
    unittest.main()
