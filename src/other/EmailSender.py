import xml.etree.cElementTree as ET

from mailer import Mailer, Message


class EmailSender:
    def __init__(self, *, buffer_size=5):
        self.mailer = Mailer('smtp.gmail.com', 587, use_tls=True)
        self.mailer.login(usr="123szukaczmieszkan123@gmail.com", pwd="#Rguih1m37x")
        self.flats_buffer = []
        self.buffer_size = buffer_size

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
            tr = ET.SubElement(table, "tr")
            ET.SubElement(tr, "img", src=photo)

        # SEPARATORS
        ET.SubElement(root, "hr")
        ET.SubElement(root, "br")
        ET.SubElement(root, "br")
        ET.SubElement(root, "hr")

    def flush(self):
        root = ET.Element("html")

        for flat in self.flats_buffer:
            flat_dict = flat.to_dict()
            self._display_to_html(flat_dict, root)

        message = Message(From="123szukaczmieszkan123@gmail.com", To="kubagros@gmail.com")
        message.Subject = f"MIESZKANIA"
        message.Html = ET.tostring(root, method='html')
        self.mailer.send(message)

    def send(self, flat):
        self.flats_buffer.append(flat)

        if len(self.flats_buffer) >= self.buffer_size:
            self.flush()
            self.flats_buffer.clear()

    def __del__(self):
        self.flush()



