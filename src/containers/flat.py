from collections import namedtuple

from selenium.common.exceptions import NoSuchElementException

from other.driver import driver

ExtractionResult = namedtuple('ExtractionResult', ['status', 'value'])

class Flat:
    def __init__(self):
        self.attributes = {}
        self.description_attributes = {}
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
        obj = cls()
        obj.url = url

        driver.get(url)

        obj.title = driver.find_element_by_class_name('myAdTitle').text
        obj.price = cls._parse_price(driver.find_element_by_class_name('price').text)
        obj.description = driver.find_element_by_class_name('description').text
        obj.address = driver.find_element_by_class_name('full-address').text

        # top menu
        sel_menu = driver.find_element_by_class_name("selMenu")
        all_sel_menu_children = sel_menu.find_elements_by_xpath("./*")
        for el in all_sel_menu_children:
            try:
                name_elem = el.find_element_by_class_name('name')
                value_elem = el.find_element_by_class_name('value')
            except NoSuchElementException:
                continue
            obj.attributes[name_elem.text] = value_elem.text

        return obj

    def extract_info_from_description(self, extractor):
        status, attribute, value = extractor(self.description)
        self.description_attributes[attribute] = ExtractionResult(status, value)
        print(self.description_attributes[attribute])
        print(self.url)
        print(self.description)