import logging
import sys
from datetime import timedelta

from filters.attribute_filter import AttributeFilter
from containers.flat import Flat
from data_provider.address_provider import address_provider
from data_provider.gumtree_flat_provider import GumtreeFlatProvider

from filters.exclude_address_filter import ExcludeAddressFilter
from other.LoopTicker import LoopTicker
from other.database import Database
from parsers.address_extractor import AddressExtractor
from parsers.bachelor_pad_extractor import BachelorPadExtractor
from parsers.interconnecting_room_extractor import InterconnectingRoomExtractor
from parsers.kitchenette_extractor import KitchenetteExtractor
from text.analysis.context_analysers.first_word_of_sentence_context import FirstWordOfSentenceContext
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext
from text.analysis.context_analysers.price_context import PriceContext


class ScrappingManager:
    def __init__(self, *, check_interval_in_seconds, filters, config, extractors, first_run_time_delta):
        self.flat_filters = filters
        self.extractors = extractors

        self._first_run_time_delta = first_run_time_delta
        self._database = Database()
        self._gumtree_flat_provider = GumtreeFlatProvider(first_run_time_delta, self._database, **config)
        self._loop_ticker = LoopTicker(check_interval_in_seconds)

    def run(self):

        logger = logging.getLogger('scrapLogger')
        logger.setLevel(logging.INFO)
        logger.propagate = False

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.info("ASDASD")
        while self._loop_ticker.tick():
            for flat_link in self._gumtree_flat_provider.get_most_recent_flat_links(): #TODO integrate with database
                try:
                    self._database.increase_processed_flats_counter()

                    logger.info("Scrapping flat started...")
                    flat = Flat.from_url(flat_link)
                    logger.info("done")


                    if not self._database.has_flat(flat):
                        logger.info("Flat not found in db yet")

                        logger.info("Extracting info from description started...")
                        flat.extract_info_from_description(self.extractors)
                        logger.info("done")

                        logger.info("saving flat to db...")
                        self._database.save_flat(flat, self.flat_filters)
                        logger.info("done")

                    else:
                        logger.info("Flat already in db. Skipping")



                except Exception as e:
                    logger.error(e, exc_info=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    without_kitchenette = AttributeFilter(KitchenetteExtractor.attribute_name, [False])
    without_interconnecting_room = AttributeFilter(InterconnectingRoomExtractor.attribute_name, [False])
    not_bachelor_pad = AttributeFilter(BachelorPadExtractor.attribute_name, [False])
    excluded_addresses_filter = ExcludeAddressFilter(["Nowa Huta", "Borek Fałęcki", "Wzgórza Krzesławickie", "Prokocim",
                                                      "Łagiewniki", "Prądnik Czerwony", "Podgórze duchackie",
                                                      "Bieńczyce", "Czyżyny", "Bieżanów", "Mistrzejowice",
                                                      "Swoszowice", "Ruczaj",

                                                      'Eliasza Radzikowskiego', 'Aleja 29 Listopada',
                                                      'Dobrego Pasterza', 'Żabiniec', 'Jana Sobieskiego', 'Białoprądnicka',

                                                      ])

    extractors = [
        AddressExtractor(address_provider, excluded_contexts=[
            FirstWordOfSentenceContext(),
            NearbyLocationContext(address_provider=address_provider),
            PriceContext()]),

        InterconnectingRoomExtractor(),
        KitchenetteExtractor(),
        BachelorPadExtractor()
    ]

    two_room_cfg = {
       'price_low': 800,
       'price_high': 1500,
       'room': 2
    }

    three_room_cfg = {
       'price_low': 1000,
       'price_high': 2200,
       'room': 3
    }

    mgr = ScrappingManager(check_interval_in_seconds=1*60*60,
                           filters=[
                               without_kitchenette,
                               without_interconnecting_room,
                               not_bachelor_pad,
                               excluded_addresses_filter
                           ],
                           extractors=extractors,
                           config=two_room_cfg,
                           first_run_time_delta=timedelta(days=4))

    mgr.run()
