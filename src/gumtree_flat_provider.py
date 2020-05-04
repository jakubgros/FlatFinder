from src.flat import Flat
from src.flat_provider import FlatProvider
from src.driver import driver


class GumtreeFlatProvider(FlatProvider):
    def __init__(self, **kwargs):
        '''
        :param kwargs:
        kwargs[price_low]
        kwargs[price_high]
        kwargs[from] = {agncy, ownr}

        '''
        self.web_url \
            = f'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/krakow/mieszkanie/v1c9008l3200208a1dwp1?pr={kwargs["price_low"]},' \
            f'{kwargs["price_high"]}&fr={kwargs["from"]}&priceType=FIXED'
        self.web_url += '&nr={page_number}'

    def raw_announce_page_generator(self):


        page_number = 0
        while True:
            current_page_url = self.web_url.format(page_number=page_number)
            driver.get(current_page_url)

            raw_announcements = driver.find_elements_by_class_name("tileV1")
            raw_announcements = [announcement.find_element_by_class_name('title') for announcement in raw_announcements]
            raw_announcements = [announcement.find_element_by_css_selector(':first-child') for announcement in raw_announcements]
            raw_announcements = [announcement.get_attribute('href') for announcement in raw_announcements]

            yield from raw_announcements
            page_number += 1

    def run(self):
        found_in_city = "Kraków"
        flats = []
        for i, url in enumerate(self.raw_announce_page_generator()):
            print(i)
            flat = Flat.from_url(url)
            flat.extract_location_from_description(found_in_city)
            flats.append(flat)
            if(i > 50):
                break