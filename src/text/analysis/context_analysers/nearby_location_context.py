import logging
from collections import defaultdict
from itertools import chain
from typing import List

from containers.address_match import AddressMatch
from data_provider.address_provider import address_provider
from parsers.address_extractor import AddressExtractor
from utilities.utilities import get_elements_before, split_on_special_characters, find_slice_beg


class NearbyLocationContext:
    def __init__(self, *, introducers=None, conjunctions=None, negate=False, address_provider):
        self.negate = negate
        self.address_provider = address_provider

        if introducers:
            self.introducers = introducers
        else:
            self.introducers = {'w sąsiedztwie'}

        self.introducers = {e.lower() for e in self.introducers}

        if conjunctions:
            self.conjunctions = conjunctions
        else:
            self.conjunctions = {'i', 'oraz'}

    def __call__(self, match: AddressMatch): #TODO cleanup
        context_end, _ = match.match_slice_position

        considered_context = match.source[:context_end]
        found_introducers = []
        for introducer in self.introducers:
            introducer = split_on_special_characters(introducer, preserve_special_characters=True)
            found_indexes = find_slice_beg(considered_context, introducer, find_all=True, case_insensitive=True)
            found_introducers.extend([(idx, introducer) for idx in found_indexes])

        found_introducers.sort(key=lambda idx_introducer: idx_introducer[0])
        if not found_introducers:
            return False if not self.negate else True

        idx_introducer_before, introducer_before = found_introducers[-1]
        idx_past_the_introducer_before = idx_introducer_before + len(introducer_before)

        conjuncted_locations = considered_context[idx_past_the_introducer_before:]
        if not conjuncted_locations:  # nearby location introducer is right before the processed location
            return True if not self.negate else False

        # check if the introducer before refers to the currently processed location
        address_extractor = AddressExtractor(self.address_provider)

        *_, matches = address_extractor(' '.join(conjuncted_locations))
        found_addresses = chain(matches.street, matches.estate, matches.district)

        match_slices = (address.match_slice_position for address in found_addresses)


        is_the_word_an_address_part_or_conjunction = [False] * len(conjuncted_locations)

        #locations
        for beg, end in match_slices:
            for i in range(beg, end):
                is_the_word_an_address_part_or_conjunction[i] = True

        #conjunctions
        for i in range(len(conjuncted_locations)):
            if is_the_word_an_address_part_or_conjunction[i]: #already matched to location
                continue
            else:
                if conjuncted_locations[i] in self.conjunctions:
                    is_the_word_an_address_part_or_conjunction[i] = True

        are_all_true = all(is_the_word_an_address_part_or_conjunction)
        return are_all_true if not self.negate else not are_all_true
