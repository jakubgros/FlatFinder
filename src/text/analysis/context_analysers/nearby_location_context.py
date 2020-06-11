from itertools import chain
from typing import List

from containers.address_match import AddressMatch
from parsers.address_extractor import AddressExtractor
from utilities.utilities import split_on_special_characters, find_slice_beg

class NearbyLocationContext:
    def __init__(self, *,
                    introducers=None,
                    conjunctions=None,
                    location_type_prefixes=None,
                    negate=False,
                    address_provider):

        self.negate = negate
        self.address_provider = address_provider

        if introducers:
            self.introducers = introducers
        else:
            self.introducers = {'w sąsiedztwie', 'w pobliżu', 'nieopodal', 'W niedalekiej odległości znajduje się',
                                'niedaleko', 'z widokiem na', 'przy samym', 'widok na', 'w bezpośrednim sąsiedztwie'
                                'metrów do', 'metry do', 'metrów od', 'metrów do',
                                'kilometrów do', 'kilometry do', 'kilometrów od', 'kilometry od',
                                'minuty do', 'minut do', 'minuty od', 'minut od', 'boczna od',
                                'Blisko przystanek autobusowy przy'}

        self.introducers = {e.lower() for e in self.introducers}

        if conjunctions:
            self.conjunctions = conjunctions
        else:
            self.conjunctions = {'i', 'oraz', ',', 'lub'}

        if location_type_prefixes:
            self.location_type_prefixes = location_type_prefixes
        else:
            self.location_type_prefixes = {'ul', 'os', 'oś'}
        self.location_type_prefixes = {e.lower() for e in self.location_type_prefixes}


    def _find_all_introducers(self, source: List[str]):
        found_introducers = []

        for introducer in self.introducers:
            introducer = split_on_special_characters(introducer, preserve_special_characters=True)
            found_indexes = find_slice_beg(source, slice_to_find=introducer, find_all=True, case_insensitive=True)
            found_introducers.extend([(idx, introducer) for idx in found_indexes])

        found_introducers.sort(key=lambda idx_introducer: idx_introducer[0])

        return found_introducers

    def _return_value(self, val):
        if not self.negate:
            return val
        else:
            return not val

    def does_introducer_refer_to_tested_location(self, introducer_subject):
        address_extractor = AddressExtractor(self.address_provider)

        *_, matches = address_extractor(introducer_subject)
        found_addresses = chain(matches.street, matches.estate, matches.district, matches.place)
        match_slices = (address.match_slice_position for address in found_addresses)

        is_the_word_an_address_part_or_conjunction = [False] * len(introducer_subject)

        # locations
        for beg, end in match_slices:
            for i in range(beg, end):
                is_the_word_an_address_part_or_conjunction[i] = True

        # conjunctions
        for i in range(len(introducer_subject)):
            if not is_the_word_an_address_part_or_conjunction[i]:
                if introducer_subject[i] in self.conjunctions:
                    is_the_word_an_address_part_or_conjunction[i] = True

        # location types
        for i in range(len(introducer_subject)):
            if not is_the_word_an_address_part_or_conjunction[i]:
                if introducer_subject[i].lower() in self.location_type_prefixes:
                    is_the_word_an_address_part_or_conjunction[i] = True
                    try:
                        if introducer_subject[i+1] == '.':
                            is_the_word_an_address_part_or_conjunction[i+1] = True
                    except IndexError:
                        pass

        # newline character
        for i in range(len(introducer_subject)):
            if not is_the_word_an_address_part_or_conjunction[i]:
                if introducer_subject[i] == '\n':
                    is_the_word_an_address_part_or_conjunction[i] = True


        return all(is_the_word_an_address_part_or_conjunction)

    def __call__(self, match: AddressMatch):
        context_end, _ = match.match_slice_position
        considered_context = match.source[:context_end]
        found_introducers = self._find_all_introducers(considered_context)
        if not found_introducers:
            return self._return_value(False)

        idx_introducer_before, introducer_before = found_introducers[-1]
        idx_past_the_introducer_before = idx_introducer_before + len(introducer_before)

        introducer_subject = considered_context[idx_past_the_introducer_before:]
        if not introducer_subject:  # nearby location introducer is right before the processed location
            return self._return_value(True)

        return self._return_value(self.does_introducer_refer_to_tested_location(introducer_subject))
