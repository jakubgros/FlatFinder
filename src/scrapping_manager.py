import logging
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
        self.gumtree_flat_provider = GumtreeFlatProvider(first_run_time_delta, **config)
        self.extractors = extractors

        self.processed_flats_by_titles = {}
        self.first_run_time_delta = first_run_time_delta
        self.output_manager = Database()
        self.loop_ticker = LoopTicker(check_interval_in_seconds)

    def apply_filters(self, flats):
        for flat_filter in self.flat_filters:
            flats = flat_filter(flats)

        return flats

    def _is_duplicate_of_already_processed(self, flat):
        return flat.title in self.processed_flats_by_titles

    def run(self):
        while self.loop_ticker.tick():
            for flat_link in self.gumtree_flat_provider.get_most_recent_flat_links():
                try:
                    flat = Flat.from_url(flat_link)

                    if not self._is_duplicate_of_already_processed(flat):
                        self.processed_flats_by_titles[flat.title] = flat

                        flat.extract_info_from_description(self.extractors)

                        new_flats = self.apply_filters([flat])
                        self.output_manager.save(new_flats)

                except Exception as e:
                    logging.error(e, exc_info=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    without_kitchenette = AttributeFilter(KitchenetteExtractor.attribute_name, [False])
    without_interconnecting_room = AttributeFilter(InterconnectingRoomExtractor.attribute_name, [False])
    not_bachelor_pad = AttributeFilter(BachelorPadExtractor.attribute_name, [False])
    excluded_addresses_filter = ExcludeAddressFilter(["Nowa Huta", "Borek Fałęcki", "Wzgórza Krzesławickie", "Prokocim",
                                                      "Łagiewniki", "Prądnik Czerwony", "Podgórze duchackie",
                                                      "Bieńczyce", "Czyżyny", "Bieżanów", "Mistrzejowice",
                                                      "Swoszowice", "Ruczaj"])

    extractors = [
        AddressExtractor(address_provider, excluded_contexts=[
            FirstWordOfSentenceContext(),
            NearbyLocationContext(address_provider=address_provider),
            PriceContext()]),

        InterconnectingRoomExtractor(),
        KitchenetteExtractor(),
        BachelorPadExtractor()
    ]

    mgr = ScrappingManager(check_interval_in_seconds=60,
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
                           extractors=extractors,
                           first_run_time_delta=timedelta(minutes=30))

    mgr.run()
