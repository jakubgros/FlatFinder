import dataclasses
import json
import logging
import shutil
import traceback
from datetime import datetime
from pprint import pprint
from random import random
from pathlib import Path

import jsonpickle as jsonpickle

from env_utils.base_dir import base_dir
from filters.attribute_filter import AttributeFilter
from containers.flat import Flat
from data_provider.address_provider import address_provider
from data_provider.gumtree_flat_provider import GumtreeFlatProvider
from timeit import default_timer as timer
import time

from filters.exclude_address_filter import ExcludeAddressFilter
from parsers.address_extractor import AddressExtractor
from parsers.bachelor_pad_extractor import BachelorPadExtractor
from parsers.interconnecting_room_extractor import InterconnectingRoomExtractor
from parsers.kitchenette_extractor import KitchenetteExtractor
from text.analysis.context_analysers.first_word_of_sentence_context import FirstWordOfSentenceContext
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext
from text.analysis.context_analysers.price_context import PriceContext

processed = 0
currently_printed_id = 0


class ScrappingManager:
    def __init__(self, *, check_interval_in_seconds, filters, config, extractors):
        self.flat_filters = filters
        self.check_interval = check_interval_in_seconds
        self.gumtree_flat_provider = GumtreeFlatProvider(**config)
        self.extractors = extractors

        self.start = timer()

        self.processed_flats_by_titles = {}
        self.flats_by_order_of_processing = []

        self.set_up_db()

    def set_up_db(self):
        db_dir = f'{base_dir}/temp/fetched_flats'
        shutil.rmtree(db_dir, ignore_errors=True)
        Path(db_dir).mkdir(parents=True, exist_ok=True)

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

    def save_to_db(self, flats):

        self.flats_by_order_of_processing.extend(flats)
        for flat in flats:
            print(json.dumps(flat.to_dict(), indent=2))


    def apply_filters(self, flats):
        for flat_filter in self.flat_filters:
            flats = flat_filter(flats)

        return flats

    def run(self):
        while True:
            try:
                for flat_link in self.gumtree_flat_provider.get_most_recent_flat_links():
                    try:
                        global processed
                        processed += 1
                        flat = Flat.from_url(flat_link)

                        if flat.title in self.processed_flats_by_titles:
                            continue
                        else:
                            self.processed_flats_by_titles[flat.title] = flat

                        flat.extract_info_from_description(self.extractors)

                        new_flats = [flat]
                        new_flats = self.apply_filters(new_flats)

                        self.save_to_db(new_flats)

                    except Exception as e:
                        logging.error(e, exc_info=True)



            except Exception as e:
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
                print(f"EXCEPTION CAUGHT:\n {e}")
                print(traceback.format_exc())
                print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

            self._wait_until_interval_passes()



if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    without_kitchenette = AttributeFilter(KitchenetteExtractor.attribute_name, [False])
    without_interconnecting_room = AttributeFilter(InterconnectingRoomExtractor.attribute_name, [False])
    not_bachelor_pad = AttributeFilter(BachelorPadExtractor.attribute_name, [False])
    excluded_addresses_filter = ExcludeAddressFilter(["Nowa Huta", "Borek Fałęcki", "Wzgórza Krzesławickie", "Prokocim",
                                                      "Łagiewniki", "Prądnik Czerwony", "Podgórze duchackie",
                                                      "Bieńczyce", "Czyżyny", "Bieżanów", "Mistrzejowice",
                                                      "Swoszowice"])

    extractors = [
        AddressExtractor(address_provider, excluded_contexts=[
            FirstWordOfSentenceContext(),
            NearbyLocationContext(address_provider=address_provider),
            PriceContext()]),

        InterconnectingRoomExtractor(),
        KitchenetteExtractor(),
        BachelorPadExtractor()
    ]

    mgr = ScrappingManager(check_interval_in_seconds=300,
                           filters=[
                               without_kitchenette,
                               without_interconnecting_room,
                               not_bachelor_pad,
                               excluded_addresses_filter
                           ],
                           config={
                               'price_low': 1000,
                               'price_high': 1500
                           },
                           extractors=extractors)

    mgr.run()
