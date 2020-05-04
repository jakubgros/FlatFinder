from selenium.common.exceptions import NoSuchElementException

from src.driver import driver


class Flat:
    def __init__(self):
        self.attributes = {}
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

    def extract_location_from_description(self, found_in_city):

        import unidecode
        found_in_city = unidecode.unidecode(found_in_city).strip().lower()
        address = unidecode.unidecode(self.address).strip().lower()

        need_to_extract = found_in_city == address

        if(not need_to_extract):
            return