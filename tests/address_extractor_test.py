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
        expected_counter = Counter(expected)
        actual_counter = Counter(actual)

        return self.assertTrue(expected_counter == actual_counter,
                               f'expected = {expected_counter}, actual = {actual_counter}')

    def testBulk(self):
        import logging
        logging.root.setLevel(logging.NOTSET)
        flat = AddressExtractorTest.all_flats[0]

        import cProfile
        pr = cProfile.Profile()
        pr.enable()

        _, _, found_address = self.extractor(flat['description'])

        pr.disable()

        from pstats import Stats
        p = Stats(pr)
        p.sort_stats('tottime').print_stats()


        #self._compareAddressResults(flat, found_address)


if __name__ == "__main__":
    unittest.main()
