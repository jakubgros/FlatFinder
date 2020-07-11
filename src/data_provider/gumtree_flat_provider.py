import logging

from containers.flat import Flat
from exception.exception import FFE_InvalidArgument

from other.driver import driver

# TODO add tests

class GumtreeFlatProvider:
    def __init__(self, **kwargs):
        """
        :param kwargs:
        kwargs[price_low]
        kwargs[price_high]
        kwargs[from]: 'agncy' or 'ownr'
        """
        args = []
        if 'price_low' in kwargs or 'price_high' in kwargs:
            low = kwargs.get('price_low', '')
            high = kwargs.get('price_high', '')
            if low > high:
                raise FFE_InvalidArgument("Price lower boundary can't be greater than higher boundary")
            args.append(f'pr={low},{high}')

        if 'from' in kwargs:
            args.append(f'fr={kwargs["from"]}')

        self.web_url \
            = 'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/krakow/v1c9008l3200208p{page_number}?'\
              + '&'.join(args)

        self.processed_flat_links = set()
        self.first_run = True

    def get_flat_links(self, page_number):
        flat_links = []
        try:
            current_page_url = self.web_url.format(page_number=page_number)
            driver.get(current_page_url)
            flat_links = driver.find_elements_by_class_name("tileV1")
            flat_links = [announcement.find_element_by_class_name('title') for announcement in
                                      flat_links]
            flat_links = [announcement.find_element_by_css_selector(':first-child') for announcement in
                                      flat_links]
            flat_links = [announcement.get_attribute('href') for announcement in flat_links]
        except Exception as e:
            logging.debug(e)
        finally:
            return set(flat_links)

    def get_most_recent_flat_links(self):
        page_number = 0

        most_recent_flat_links = []
        while True:
            page_number += 1
            curr_page_links = self.get_flat_links(page_number)

            new_links = curr_page_links.difference(self.processed_flat_links)

            most_recent_flat_links.extend(new_links)
            self.processed_flat_links.update(new_links)

            if len(new_links) != len(curr_page_links) or self.first_run:
                self.first_run = False
                break

        return most_recent_flat_links

