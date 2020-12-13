import logging
from datetime import datetime
from datetime import timedelta
from selenium.common.exceptions import NoSuchElementException

from containers.flat import Flat
from exception.exception import FFE_InvalidArgument

from other.driver import driver

# TODO add tests

class GumtreeFlatProvider:
    def __init__(self, first_run_time_delta, database, **kwargs):
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

        if 'room' in kwargs:
            args.append(f'nr={kwargs["room"]}')

        self.web_url \
            = 'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/krakow/v1c9008l3200208p{page_number}?'\
              + '&'.join(args)

        self.database = database
        self.first_run = True

        self.oldest_add_date_to_fetch_on_first_run = datetime.now() - first_run_time_delta
        self.first_search_depth_reached = False


    def _to_date(self, when_added):
        origin = when_added
        when_added = when_added.replace('temu', '')
        when_added = when_added.strip()
        when_added = when_added.split()

        if len(when_added) == 1:
            amount = 1
            unit = when_added[0]
        elif len(when_added) == 2:
            amount, unit = when_added
        else:
            raise Exception(f"date in unexpected format: '{origin}'")

        if unit.startswith("d"):
            unit = "days"
        elif unit.startswith("m"):
            unit = "minutes"
        elif unit.startswith("g"):
            unit = "hours"
        else:
            raise Exception(f"unparsable unit: {unit}")

        date = datetime.now() - timedelta(**{unit: int(amount)})

        return date

    def get_flat_links_with_date_added(self, page_number):

        flat_links = []
        try:
            current_page_url = self.web_url.format(page_number=page_number)
            driver.get(current_page_url)
            flat_tiles = driver.find_elements_by_class_name("tileV1")

            for tile in flat_tiles:
                link = tile.find_element_by_class_name('title').find_element_by_css_selector(':first-child').get_attribute('href')

                try:
                    when_added = tile.find_element_by_class_name('info').find_element_by_class_name('creation-date').text
                except NoSuchElementException:
                    when_added = None
                else:
                    when_added = self._to_date(when_added)

                is_featured = when_added is None

                flat_links.append((is_featured, link, when_added))

        except Exception as e:
            logging.debug(e)
        finally:
            return flat_links

    def get_most_recent_flat_links(self):
        page_number = 0

        most_recent_flat_links = []

        has_duplicated = False
        while True:
            page_number += 1

            curr_page_links = self.get_flat_links_with_date_added(page_number)

            new_links = []
            for is_featured, link, when_added in curr_page_links:
                if when_added and when_added < self.oldest_add_date_to_fetch_on_first_run:
                    self.first_search_depth_reached = True
                    break

                if self.database.has_link(link) and not is_featured: #the same featured link may occur on many pages
                    has_duplicated = True

                if not self.database.has_link(link):
                    new_links.append(link)
                    self.database.save_link(link)

            most_recent_flat_links.extend(new_links)

            if self.first_search_depth_reached and self.first_run:
                self.first_run = False
                break

            if has_duplicated:
                break

        return most_recent_flat_links

