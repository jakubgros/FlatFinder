import unittest

from src.address_provider import AddressProvider
from src.extractor import AddressExtractor

import xml.etree.ElementTree as ET


class AddressExtractorTest(unittest.TestCase):
    all_flats = []

    @classmethod
    def setUpClass(cls):
        tree = ET.parse('../data/tagged/addresses_from_title_and_description.xml')

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

    def testBulk(self):
        print()

        flat = AddressExtractorTest.all_flats[0]
        print(flat['description'])
        status, attribute, value = self.extractor(flat['description'])
        pass









if __name__ == '__main__':
    unittest.main()