import unittest
from collections import Counter

from src.address_provider import AddressProvider
from src.extractor import AddressExtractor

import xml.etree.ElementTree as ET


class AddressExtractorTest(unittest.TestCase):
    all_flats = []

    @classmethod
    def setUpClass(cls):
        tree = ET.parse('../data/tagged/addresses_from_title_and_description/addresses_from_title_and_description.xml')

        root = tree.getroot()

        for flatXml in root:
            title = flatXml.find('title').text
            url = flatXml.find('url').text
            description = flatXml.find('description').text
            locations_node = flatXml.find('locations')
            locations = [location.text for location in locations_node]
            cls.all_flats.append({'title': title,
                              'url': url,
                              'description': description,
                              'locations': locations})

    def setUp(self):
        self.extractor = AddressExtractor(AddressProvider.Instance())

    def testCaseMatters(self):
        status, *_ = self.extractor("Oferuję do wynajęcia śliczne mieszkanie 4-pokojowe") # won't match "Śliczna" street
        self.assertFalse(status)

    def _compareAddressResults(self, flat, found_address):
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

    def testRegression(self): #TODO once all passes in testBulk, change compareAddressResult to more strict comparison
        import logging
        logging.root.setLevel(logging.NOTSET)
        passing_tests = [AddressExtractorTest.all_flats[i] for i in [0, 1, 4, 5, 13, 20, 23, 24, 27, 28, 36, 37, 43, 48, 50]]
        for i, flat in enumerate(passing_tests):
            _, _, found_address = self.extractor(flat['title'] + flat['description'])
            self._compareAddressResults(flat, found_address)

    def testBulk(self):
        import logging
        logging.root.setLevel(logging.NOTSET)

        for i, flat in enumerate(AddressExtractorTest.all_flats):
            with self.subTest(i=i):
                _, _, found_address = self.extractor(flat['title'] + flat['description'])
                self._compareAddressResults(flat, found_address)

if __name__ == "__main__":
    unittest.main()
