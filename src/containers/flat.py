import json
import traceback
import unicodedata
from collections import namedtuple

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

from other.driver import driver

DISABLE_PARALLELIZED_COMPUTATION = True
if DISABLE_PARALLELIZED_COMPUTATION:
    import multiprocess.dummy as mp
else:
    import multiprocess as mp

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
        self.photos = None

    @staticmethod
    def _parse_price(price_as_string):
        price_stripped = ''.join([c for c in price_as_string if c in '1234567890'])
        return int(price_stripped)

    def _extract_photo_links(self, page_src):
        bs = BeautifulSoup(page_src, features='html.parser')

        gallery = bs.find('div', class_="vip-gallery")
        thumbsnails = gallery.find(class_="thumbs").find_all('img')
        thumbsnails_links = [elem['src'] for elem in thumbsnails]

        photo_links = []
        for thumbsnail_link in thumbsnails_links:
            proper_link_beg = thumbsnail_link.find('i.ebayimg.com')
            proper_link_end = thumbsnail_link.rfind('/')
            proper_link = thumbsnail_link[proper_link_beg:proper_link_end] + "/$_20.JPG"
            photo_links.append(proper_link)

        return photo_links

    @classmethod
    def from_url(cls, url):
        flat = cls()
        flat.url = url

        driver.get(url)

        flat.title = unicodedata.normalize('NFKC', driver.find_element_by_class_name('myAdTitle').text)
        flat.price = cls._parse_price(driver.find_element_by_class_name('price').text)
        flat.description = unicodedata.normalize('NFKC', driver.find_element_by_class_name('description').text)
        flat.address = unicodedata.normalize('NFKC', driver.find_element_by_class_name('full-address').text)

        flat.photos = flat._extract_photo_links(driver.page_source)

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
        def runner(extractor):
            try:
                extracted_val = extractor(self.title + '.\n' + self.description)
                return extractor.attribute_name, extracted_val
            except Exception as e:
                trace = traceback.format_exc()
                return extractor.attribute_name, Exception(str(e) + '\n' + trace)

        with mp.Pool() as pool:
            extracted = pool.map(runner, extractors)

        for attribute_name, extracted_val in extracted:
            if isinstance(extracted_val, Exception):
                raise extracted_val
            else:
                self.description_extracted_attributes[attribute_name] = extracted_val

    def to_dict(self):
        as_dict = {
            'title': self.title,
            'attributes': self.attributes,
            'description': self.description,
            'url': self.url,
            'address': self.address,
            'price': self.price,
            'photos': self.photos,
        }

        descr_extr_attr_as_dict = {}

        for attr_name, val in self.description_extracted_attributes.items():
            val_as_dict = None
            try:
                val_as_dict = val.to_dict()
            except AttributeError:
                pass

            if not val_as_dict:
                val_as_dict = val

                if isinstance(val_as_dict, set):
                    val_as_dict = list(val_as_dict)

            descr_extr_attr_as_dict[attr_name] = val_as_dict


        as_dict['description_extracted_attributes'] = descr_extr_attr_as_dict

        return as_dict
