import logging
import typing
from dataclasses import dataclass
from typing import List, Union

from colorama import Fore, Style

from comparators.comparison_rules.comparison_rule import ComparisonRule
from comparators.comparison_rules.comparison_rule_type import ComparisonRuleType
from comparators.comparison_rules.comparison_rules_container import ComparisonRulesContainer
from comparators.morphologic_comparator import MorphologicComparator
from comparators.name_comparator import NameComparator
from containers.address_match import AddressMatch
from text.text_searcher import TextSearcher

from itertools import chain
from text.analysis.tagger import tagger
from utilities.utilities import do_slices_overlap, slice_span


@dataclass
class Address:
    district: List[AddressMatch]
    estate: List[AddressMatch]
    street: List[AddressMatch]
    place: List[AddressMatch]

    @property
    def all(self):
        return self.district + self.estate + self.street + self.place

    @property
    def all_addresses(self):
        return self.district + self.estate + self.street


class AddressExtractor:
    def __init__(self, address_provider, excluded_contexts=[]):
        self.address_provider = address_provider
        self.attribute_name = "address"

        self.comparison_rules = ComparisonRulesContainer([
            ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY)
        ])

        self.excluded_contexts = excluded_contexts

    @staticmethod
    def _extract_street_number(words_list, matched_location_slice_pos):
        slice_beg, slice_end = matched_location_slice_pos

        try:
            unit_number_slice = (slice_end, slice_end + 1)
            street_number = int(" ".join(words_list[slice(*unit_number_slice)]))
        except (IndexError, ValueError):
            return False, None, None
        else:

            return True, unit_number_slice, street_number

    def _get_comparator(self, location_name):
        if tagger.does_contain_person_first_name(location_name):
            comparator = NameComparator(ignore_case_sensitivity_if_actual_upper_case=True)
        else:
            comparator = MorphologicComparator(comparison_rules=self.comparison_rules,
                                               title_case_sensitive=True,
                                               ignore_case_sensitivity_if_actual_upper_case=True)

        return comparator.equals

    def _match_locations(self, all_locations, description):
        all_matched_locations = []

        for location in all_locations:
            for location_name in [location["official"], *location["colloquial"]]:

                does_contain, (match_slice_pos, all_words) = TextSearcher.find(
                    phrase_to_find=location_name,
                    text=description,
                    equality_comparator=self._get_comparator(location_name))

                if does_contain:
                    match = AddressMatch(
                        location=location['official'],
                        match_slice_position=match_slice_pos,
                        source=all_words)

                    all_matched_locations.append(match)

        return all_matched_locations

    def _should_be_excluded(self, match):
        for ctx_analyser in self.excluded_contexts:
            if ctx_analyser(match):
                logging.debug(
                    f"\nexcluded by {ctx_analyser.__class__.__name__}: \n {match} \n {match.source[slice(*match.match_slice_position)]}\n")
                return True

        return False

    def _filter_by_context(self, address):
        # filter by context analysers
        address.district = [match for match in address.district if not self._should_be_excluded(match)]
        address.estate = [match for match in address.estate if not self._should_be_excluded(match)]
        address.street = [match for match in address.street if not self._should_be_excluded(match)]

    @staticmethod
    def _overlaps_with_bigger_match(the_match, all_matches):
        for other_match in all_matches:
            the_match_slice = the_match.match_slice_position
            other_match_slice = other_match.match_slice_position

            if do_slices_overlap(the_match_slice, other_match_slice) \
                    and slice_span(the_match_slice) < slice_span(other_match_slice):
                return True
        return False

    def _filter_overlapping(self, address):
        address.street = [match for match in address.street
                          if not self._overlaps_with_bigger_match(match, address.all)]
        address.estate = [match for match in address.estate
                          if not self._overlaps_with_bigger_match(match, address.all)]
        address.district = [match for match in address.district
                            if not self._overlaps_with_bigger_match(match, address.all)]
        address.place = [match for match in address.place
                         if not self._overlaps_with_bigger_match(match, address.all)]

    def __call__(self, description: Union[List[str], str]):
        """ Extracts location from description, returns (status, extracted_attribute_name, value) """
        address = Address(district=self._match_locations(self.address_provider.districts, description),
                          estate=self._match_locations(self.address_provider.estates, description),
                          street=self._match_locations(self.address_provider.streets, description),
                          place=self._match_locations(self.address_provider.places, description))

        ''' in case two addresses were matched to the same piece of text we accept the longer 
        e.g. "Galeria Bronowicka" might be matched to both "Bronowicka" street and "Galeria Bronowicka" place. 
        By doing the overlap filtering we remove the unwanted street match '''
        self._filter_overlapping(address)

        self._filter_by_context(address)

        for match in address.street:
            success, _, street_number = self._extract_street_number(match.source, match.match_slice_position)
            if success:
                match.location += " " + str(street_number)

        # noinspection PyUnreachableCode
        if __debug__:
            for match in chain(address.district, address.estate, address.street, address.place):
                source = match.source[:]
                source[slice(*match.match_slice_position)] = [
                    Fore.GREEN + ' '.join(source[slice(*match.match_slice_position)]) + Style.RESET_ALL]
                description = ' '.join(source)
                logging.debug(f"\nMatched db location '{match.location}' to '{match.matched_phrase}'\n"
                              f"description: {description}\n")

        return len(address.all) > 0, self.attribute_name, address
