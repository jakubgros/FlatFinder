import logging
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Tuple

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

Address = namedtuple('Address', ['district', 'estate', 'street'])


class AddressExtractor:
    def __init__(self, address_provider, context_analysers=[]):
        self.address_provider = address_provider
        self.attribute_name = "address"

        self.comparison_rules = ComparisonRulesContainer([
            ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY)
        ])

        self.context_analysers = context_analysers

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

    def __call__(self, description: str):
        """ Extracts location from description, returns (status, extracted_attribute_name, value) """
        matched_districts = [match for match in self._match_locations(self.address_provider.districts, description)
                             if all([ctx_analyser(match) for ctx_analyser in self.context_analysers])]
        matched_estates = [match for match in self._match_locations(self.address_provider.estates, description)
                           if all([ctx_analyser(match) for ctx_analyser in self.context_analysers])]
        matched_streets = [match for match in self._match_locations(self.address_provider.streets, description)
                           if all([ctx_analyser(match) for ctx_analyser in self.context_analysers])]

        for match in matched_streets:
            success, _, street_number = self._extract_street_number(match.source, match.match_slice_position)
            if success:
                match.location += " " + str(street_number)

        # noinspection PyUnreachableCode
        if __debug__:
            for match in chain(matched_districts, matched_estates, matched_streets):
                source = match.source[:]
                source[slice(*match.match_slice_position)] = [
                    Fore.GREEN + ' '.join(source[slice(*match.match_slice_position)]) + Style.RESET_ALL]
                description = ' '.join(source)
                logging.debug(f"\nMatched db location '{match.location}' to '{match.matched_phrase}'\n"
                              f"description: {description}\n")

        address = Address(district=matched_districts,
                          estate=matched_estates,
                          street=matched_streets)

        return bool(matched_districts or matched_estates or matched_streets), self.attribute_name, address
