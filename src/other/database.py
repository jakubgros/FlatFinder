from pprint import pprint
import xml.etree.cElementTree as ET
from mailer import Mailer
from mailer import Message


class Database:
    def __init__(self):
        self.mailer = Mailer('smtp.gmail.com', 587, use_tls=True)
        self.mailer.login(usr="123szukaczmieszkan123@gmail.com", pwd="#Rguih1m37x")
        self.amount_of_all_processed = 0
        self.currently_printed_id = 0
        self.buffer = []
        self.buffer_size = 10

        self._processed_flats_by_titles = {}

    def save(self, flats):
        for flat in flats:
            self._processed_flats_by_titles[flat.title] = flat
            self.buffer.append(flat)

            if len(self.buffer) >= self.buffer_size:
                self.flush()

    def flush(self):

        self._save_to_email(self.buffer)
        self._save_to_console(self.buffer)


        self.buffer.clear()

    @staticmethod
    def _save_to_console(flats):
        for flat in flats:
            pprint(flat.to_dict(), indent=2)

    def _save_to_email(self, flats):
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

    @staticmethod
    def _display_to_html(flat_dict, root):
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

    def has_flat(self, flat):
        return flat.title in self._processed_flats_by_titles
