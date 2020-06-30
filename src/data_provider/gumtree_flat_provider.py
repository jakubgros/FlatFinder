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

    @property
    def most_recent_flat_links(self):
        try:
            page_number = 1
            current_page_url = self.web_url.format(page_number=page_number)
            driver.get(current_page_url)
            raw_announcements = driver.find_elements_by_class_name("tileV1")
            raw_announcements = [announcement.find_element_by_class_name('title') for announcement in
                                 raw_announcements]
            raw_announcements = [announcement.find_element_by_css_selector(':first-child') for announcement in
                                 raw_announcements]
            raw_announcements = [announcement.get_attribute('href') for announcement in raw_announcements]

            yield from raw_announcements
        except Exception as e:
            logging.debug(e)
            logging.debug(current_page_url)
            logging.debug(driver)
            raise
