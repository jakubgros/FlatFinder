import unicodedata
from collections import namedtuple

from selenium.common.exceptions import NoSuchElementException

from other.driver import driver

ExtractionResult = namedtuple('ExtractionResult', ['status', 'value'])


class Flat:
    def __init__(self):
        self.attributes = {}
        self.description_extracted_attributes = {}
        self.title = None
        self.url = None
        self.price = None
        self.description = None
        self.address = None

    @staticmethod
    def _parse_price(price_as_string):
        price_stripped = ''.join([c for c in price_as_string if c in '1234567890'])
        return int(price_stripped)

    @classmethod
    def from_url(cls, url):
        flat = cls()
        flat.url = url

        driver.get(url)

        flat.title = unicodedata.normalize('NFKC', driver.find_element_by_class_name('myAdTitle').text)
        flat.price = cls._parse_price(driver.find_element_by_class_name('price').text)
        flat.description = unicodedata.normalize('NFKC', driver.find_element_by_class_name('description').text)
        flat.address = unicodedata.normalize('NFKC', driver.find_element_by_class_name('full-address').text)

        # top menu
        sel_menu = driver.find_element_by_class_name("selMenu")
        all_sel_menu_children = sel_menu.find_elements_by_xpath("./*")
        for el in all_sel_menu_children:
            try:
                name_elem = el.find_element_by_class_name('name')
                value_elem = el.find_element_by_class_name('value')
            except NoSuchElementException:
                continue
            flat.attributes[name_elem.text] = unicodedata.normalize('NFKC', value_elem.text)

        # TODO add unicode processing
        return flat

    def extract_info_from_description(self, extractors):
        for extractor in extractors:
            value = extractor(self.description)
            self.description_extracted_attributes[extractor.attribute_name] = value
