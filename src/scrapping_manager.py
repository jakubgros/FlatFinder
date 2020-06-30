import traceback
from random import random

from attribute_filter import AttributeFilter
from containers.flat import Flat
from data_provider.address_provider import address_provider
from data_provider.gumtree_flat_provider import GumtreeFlatProvider
from timeit import default_timer as timer
import time

from parsers.address_extractor import AddressExtractor
from parsers.interconnecting_room_extractor import InterconnectingRoomExtractor
from parsers.kitchenette_extractor import KitchenetteExtractor
from text.analysis.context_analysers.first_word_of_sentence_context import FirstWordOfSentenceContext
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext
from text.analysis.context_analysers.price_context import PriceContext


class ScrappingManager:
    def __init__(self, check_interval, filters, config):
        self.attribute_filters = filters
        self.check_interval = check_interval
        self.gumtree_flat_provider = GumtreeFlatProvider(**config)
        self.processed_flat_links = set()

        self.extractors = [
            #AddressExtractor(address_provider, excluded_contexts=[
             #   FirstWordOfSentenceContext(),
             #   NearbyLocationContext(address_provider=address_provider),
            #   PriceContext()]),

            InterconnectingRoomExtractor(),
            KitchenetteExtractor()
        ]

        self.start = timer()

    def _get_new_flat_links(self):
        fetched_flat_links = set(self.gumtree_flat_provider.most_recent_flat_links)
        new_flat_links = fetched_flat_links.difference(self.processed_flat_links)
        self.processed_flat_links.update(new_flat_links)
        return new_flat_links

    def _filter_and_print(self, flat):
        filtered_data = {}
        for attribute_filter in self.attribute_filters:
            filtered_data[attribute_filter.name] = attribute_filter(flat)

        if all(len(filtered_value) > 0 for filtered_value in filtered_data.values()):
            print("FOUND FLAT MATCHING ALL FILTERS!")
        else:
            print("FLAT DOESN'T MATCH FILTERS")

        print(f'{flat.url}\n'
              f'{filtered_data}\n\n\n')

    def _get_interval(self):  # to look more like a human
        max_incline = 0.15
        current_incline = random() * max_incline
        current_incline_in_seconds = self.check_interval * current_incline

        if random() > 0.5:
            random_val = self.check_interval + current_incline_in_seconds
        else:
            random_val = self.check_interval - current_incline_in_seconds

        return random_val

    def _wait_until_interval_passes(self):
        end = timer()
        time_passed_in_seconds = end - self.start
        time_left_in_the_interval = self._get_interval() - time_passed_in_seconds
        if time_left_in_the_interval > 0:
            time.sleep(time_left_in_the_interval)

        self.start = timer()

    def run(self):
        while True:
            try:
                processed_flats = {}

                for flat_link in self._get_new_flat_links():
                    flat = Flat.from_url(flat_link)
                    flat.extract_info_from_description(self.extractors)

                    if flat.title not in processed_flats:
                        processed_flats[flat.title] = flat
                        self._filter_and_print(flat)

            except Exception as e:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
                print(f"EXCEPTION CAUGHT:\n {e}")
                print(traceback.format_exc())
                print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

        self._wait_until_interval_passes()


if __name__ == "__main__":
    without_kitchenette = AttributeFilter(KitchenetteExtractor.attribute_name, [False])
    without_interconnecting_room = AttributeFilter(InterconnectingRoomExtractor.attribute_name, [False])

    mgr = ScrappingManager(check_interval=1 * 60,
                           filters=[
                               without_kitchenette,
                               without_interconnecting_room
                           ],
                           config={
                               'price_low': 1000,
                               'price_high': 2000
                           })

    mgr.run()
