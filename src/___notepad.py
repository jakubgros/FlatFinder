from src.flat import Flat
from src.gumtree_flat_provider import GumtreeFlatProvider
from xml.etree import ElementTree as ET

def generate_description_title_data_for_address_tagging():
    args = {
        "price_low": 100,
        "price_high": 2000,
        "from": 'ownr'
    }

    provider = GumtreeFlatProvider(**args)

    root = ET.Element('flats')
    for i, url in enumerate(provider.raw_announce_page_generator()):
        if i > 100:
            break
        print(i)
        flat = Flat.from_url(url)
        flat_element = ET.SubElement(root, 'flat')
        ET.SubElement(flat_element, 'title').text = flat.title
        ET.SubElement(flat_element, 'url').text = flat.url
        ET.SubElement(flat_element, 'description').text = flat.description
        location_element = ET.SubElement(flat_element, 'locations')
        ET.SubElement(location_element, 'location').text=' '

    tree = ET.ElementTree(root)
    tree.write('thexml.xml')


import morfeusz2

morf = morfeusz2.Morfeusz(dict_path=r'..\third parties\morfeusz2-dictionary-polimorf',
                               dict_name="polimorf")

kraka = morf.analyse("kraka")
krakow = morf.analyse("kraków")
pass