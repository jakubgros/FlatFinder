import logging
from itertools import chain

from containers.address_match import AddressMatch
from data_provider.address_provider import address_provider
from parsers.address_extractor import AddressExtractor
from utilities.utilities import get_elements_before, split_on_special_characters


class NearbyLocationContext:
    def __init__(self, negate=False):
        self.negate = negate

    def __call__(self, match: AddressMatch):
        context_end, _ = match.match_slice_position

        nearby_location_introducers = {'w sąsiedztwie'}

        possible_conjunctions = {'i', 'oraz'}

        conjunction_found = False
        for conjuntion in possible_conjunctions:
            conjuntion = split_on_special_characters(conjuntion, preserve_special_characters=True)
            elements_before = get_elements_before(idx=context_end, amount=len(conjuntion), the_list=match.source,
                                                  ignored_values=['\n'])
            if conjuntion == elements_before:
                conjunction_found = True
                break

        possible_context_ends = [context_end]
        if conjunction_found:
            address_extractor = AddressExtractor(address_provider)

            has_found, _, conjuncted_addresses = address_extractor(' '.join(match.source[:context_end]))

            if not has_found:
                logging.debug(f"conjunction found but could not match location before:\n{match.source[:context_end]}")
                return False

            possible_context_ends.extend(
                [context_end - len(location) for location in
                 chain(conjuncted_addresses.district, conjuncted_addresses.estate, conjuncted_addresses.street)])

        for context_end in possible_context_ends:
            for introducer in nearby_location_introducers:
                introducer = split_on_special_characters(introducer, preserve_special_characters=True)

                elements_before = get_elements_before(idx=context_end, amount=len(introducer), the_list=match.source,
                                                      ignored_values=['\n'])

                if elements_before == introducer:
                    return True if not self.negate else False

        return False if not self.negate else True

