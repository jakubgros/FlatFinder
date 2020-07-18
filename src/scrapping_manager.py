import logging
from datetime import timedelta
from pprint import pprint
import xml.etree.cElementTree as ET
from mailer import Mailer
from mailer import Message
from filters.attribute_filter import AttributeFilter
from containers.flat import Flat
from data_provider.address_provider import address_provider
from data_provider.gumtree_flat_provider import GumtreeFlatProvider


from filters.exclude_address_filter import ExcludeAddressFilter
from other.LoopTicker import LoopTicker
from parsers.address_extractor import AddressExtractor
from parsers.bachelor_pad_extractor import BachelorPadExtractor
from parsers.interconnecting_room_extractor import InterconnectingRoomExtractor
from parsers.kitchenette_extractor import KitchenetteExtractor
from text.analysis.context_analysers.first_word_of_sentence_context import FirstWordOfSentenceContext
from text.analysis.context_analysers.nearby_location_context import NearbyLocationContext
from text.analysis.context_analysers.price_context import PriceContext

class OutputManager():
    def __init__(self):
        self.mailer = Mailer('smtp.gmail.com', 587, use_tls=True)
        self.mailer.login(usr="123szukaczmieszkan123@gmail.com", pwd="#Rguih1m37x")
        self.amount_of_all_processed = 0
        self.currently_printed_id = 0
        self.buffer = []
        self.buffer_size = 10

    def output(self, flats):
        for flat in flats:
            self.buffer.append(flat)

            if len(self.buffer) >= self.buffer_size:
                self._output_to_email(self.buffer)
                self._output_to_console(self.buffer)

                self.buffer.clear()

    def _output_to_console(self, flats):
        for flat in flats:
            pprint(flat.to_dict(), indent=2)

    def _output_to_email(self, flats):
        root = ET.Element("html")

        previous_id = self.currently_printed_id
        self.currently_printed_id += len(flats)
        for flat in flats:
            flat_dict = flat.to_dict()
            self._display_to_html(flat_dict, root)

        message = Message(From="123szukaczmieszkan123@gmail.com", To="kubagros@gmail.com")
        message.Subject = f"MIESZKANIA [{previous_id}-{self.currently_printed_id}/{self.amount_of_all_processed}]"
        message.Html = ET.tostring(root, method='html')
        self.mailer.send(message)

    def _display_to_html(self, flat_dict, root):
        address_attr = flat_dict['attributes'].get("Lokalizacja", "")
        gmaps_attr = flat_dict['address']
        extracted_addr = [addr for addr in flat_dict['description_extracted_attributes']['address'].values()]

        table = ET.SubElement(root, "table", style="border: 1px solid black; background-color: #E9967A")

        for label, value in [
            ('title', flat_dict['title']),
            ('price', flat_dict['price']),
            ('address_attr', address_attr),
            ('gmaps_attr', gmaps_attr),
            ('extracted_addr', extracted_addr),
            ('gmaps_attr', gmaps_attr),
            ('description', flat_dict['description']),
            ('link', flat_dict['url']),
        ]:
            label = str(label)
            value = str(value)
            tr = ET.SubElement(table, "tr")
            ET.SubElement(tr, "td").text = label
            ET.SubElement(tr, "td").text = value

        for photo in flat_dict['photos']:
            tr = ET.SubElement(root, "tr")
            ET.SubElement(tr, "img", src=photo)

        # SEPARATORS
        ET.SubElement(root, "hr")
        ET.SubElement(root, "br")
        ET.SubElement(root, "br")
        ET.SubElement(root, "hr")



class ScrappingManager:
    def __init__(self, *, check_interval_in_seconds, filters, config, extractors, first_run_time_delta):
        self.flat_filters = filters
        self.gumtree_flat_provider = GumtreeFlatProvider(first_run_time_delta, **config)
        self.extractors = extractors

        self.processed_flats_by_titles = {}
        self.first_run_time_delta = first_run_time_delta
        self.output_manager = OutputManager()
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
                        self.output_manager.output(new_flats)

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
