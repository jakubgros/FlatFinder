import traceback
from datetime import datetime
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
    def __init__(self, check_interval_in_seconds, filters, config, extractors):
        self.flat_filters = filters
        self.check_interval = check_interval_in_seconds
        self.gumtree_flat_provider = GumtreeFlatProvider(**config)
        self.extractors = extractors

        self.start = timer()

        self.processed_flats_by_titles = {}

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

    def announce(self, flats):
        for flat in flats:
            print(f'[{datetime.now()}]\n')
            print(flat.__dict__)
            print('\n\n\n')

    def apply_filters(self, flats):
        for flat_filter in self.flat_filters:
            flats = flat_filter(flats)

        return flats

    def run(self):
        while True:
            try:
                new_flats = []

                for flat_link in self.gumtree_flat_provider.get_most_recent_flat_links():
                    flat = Flat.from_url(flat_link)

                    if flat.title in self.processed_flats_by_titles:
                        continue
                    else:
                        self.processed_flats_by_titles[flat.title] = flat

                    flat.extract_info_from_description(self.extractors)

                    new_flats.append(flat)

                new_flats = self.apply_filters(new_flats)
                self.announce(new_flats)

            except Exception as e:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
                print(f"EXCEPTION CAUGHT:\n {e}")
                print(traceback.format_exc())
                print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

            self._wait_until_interval_passes()


if __name__ == "__main__":
    without_kitchenette = AttributeFilter(KitchenetteExtractor.attribute_name, [False])
    without_interconnecting_room = AttributeFilter(InterconnectingRoomExtractor.attribute_name, [False])

    extractors = [
        #AddressExtractor(address_provider, excluded_contexts=[
        #    FirstWordOfSentenceContext(),
        #    NearbyLocationContext(address_provider=address_provider),
         #   PriceContext()]),

        InterconnectingRoomExtractor(),
        KitchenetteExtractor()
    ]

    mgr = ScrappingManager(check_interval_in_seconds=60,
                           filters=[
                               without_kitchenette,
                               without_interconnecting_room
                           ],
                           config={
                               'price_low': 1000,
                               'price_high': 2000
                           },
                           extractors=extractors)

    mgr.run()
