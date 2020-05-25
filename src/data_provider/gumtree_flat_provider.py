import logging

from containers.flat import Flat

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
        self.web_url \
            = f'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/krakow/mieszkanie/v1c9008l3200208a1dwp1?' \
              f'pr={kwargs["price_low"]},{kwargs["price_high"]}&fr={kwargs["from"]}&priceType=FIXED' \
              '&nr={page_number}'

    @property
    def announcements(self):
        try:
            page_number = 0
            while True:
                current_page_url = self.web_url.format(page_number=page_number)
                driver.get(current_page_url)
                raw_announcements = driver.find_elements_by_class_name("tileV1")
                raw_announcements = [announcement.find_element_by_class_name('title') for announcement in
                                     raw_announcements]
                raw_announcements = [announcement.find_element_by_css_selector(':first-child') for announcement in
                                     raw_announcements]
                raw_announcements = [announcement.get_attribute('href') for announcement in raw_announcements]

                yield from raw_announcements
                page_number += 1
        except Exception as e:
            logging.debug(e)
            logging.debug(current_page_url)
            logging.debug(driver)
            raise

    def fetch(self, amount):

        fetched_flats = []
        for url in self.announcements:
            try:
                if len(fetched_flats) >= amount:
                    break

                logging.debug(f"fetching flat [{len(fetched_flats)}/{amount}]")
                new_flat = Flat.from_url(url)

                has_already_fetched = 0 != len(
                    [fetched for fetched in fetched_flats if fetched.title == new_flat.title])

                if not has_already_fetched:
                    fetched_flats.append(new_flat)

            except Exception as e:
                logging.debug(e)

        return fetched_flats
