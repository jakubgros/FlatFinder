import logging
from collections import namedtuple
from colorama import Fore, Back, Style

from comparators.comparison_rules.comparison_rule import ComparisonRule
from comparators.comparison_rules.comparison_rule_type import ComparisonRuleType
from comparators.comparison_rules.comparison_rules_container import ComparisonRulesContainer
from comparators.morphologic_comparator import MorphologicComparator
from comparators.name_comparator import NameComparator
from text.text_searcher import TextSearcher
from text.analysis.tagger import Tagger
from itertools import chain

Address = namedtuple('Address', ['district', 'estate', 'street'])


class AddressExtractor:
    def __init__(self, address_provider):
        self.address_provider = address_provider
        self.attribute_name = "address"

        self.comparison_rules = ComparisonRulesContainer([
            ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY)
        ])

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
        if Tagger.Instance().does_contain_person_first_name(location_name):
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
                    all_matched_locations.append((location["official"], match_slice_pos, all_words))

        return all_matched_locations

    def __call__(self, description):
        """ Extracts location from description, returns (status, extracted_attribute_name, value) """
        matched_districts = self._match_locations(self.address_provider.districts, description)
        matched_estates = self._match_locations(self.address_provider.estates, description)
        matched_streets = self._match_locations(self.address_provider.streets, description)

        for i, (street, match_slice_pos, all_words) in enumerate(matched_streets):
            success, unit_number_slice, street_number = self._extract_street_number(all_words, match_slice_pos)
            if success:
                street = street + " " + str(street_number)
                matched_streets[i] = (street, match_slice_pos, all_words)

        districts = [location for location, *_ in matched_districts]
        estates = [location for location, *_ in matched_estates]
        streets = [location for location, *_ in matched_streets]

        # noinspection PyUnreachableCode
        if __debug__:
            for matched_location, match_slice_pos, all_words in chain(matched_districts, matched_estates, matched_streets):
                all_words = all_words[:]
                match_slice_beg, match_slice_end = match_slice_pos
                piece_of_text_that_matched = ' '.join(all_words[match_slice_beg:match_slice_end])
                all_words[match_slice_beg:match_slice_end] = [Fore.GREEN + ' '.join(all_words[match_slice_beg:match_slice_end]) + Style.RESET_ALL]
                description = ' '.join(all_words)
                logging.debug(f"\nMatched db location '{matched_location}' to '{piece_of_text_that_matched}'\n"
                          f"description: {description}\n")

        address = Address(district=districts,
                          estate=estates,
                          street=streets)

        return bool(districts or estates or streets), self.attribute_name, address
