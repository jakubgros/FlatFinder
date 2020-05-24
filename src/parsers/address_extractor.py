import logging
from collections import namedtuple

from comparators.comparison_rules.comparison_rule import ComparisonRule
from comparators.comparison_rules.comparison_rule_type import ComparisonRuleType
from comparators.comparison_rules.comparison_rules_container import ComparisonRulesContainer
from comparators.morphologic_comparator import MorphologicComparator
from comparators.name_comparator import NameComparator
from text.TextSearcher import TextSearcher
from text.analysis.Tagger import Tagger

Address = namedtuple('Address', ['district', 'estate', 'street'])


class AddressExtractor:
    def __init__(self, address_provider):
        self.address_provider = address_provider
        self.attribute_name = "address"

        self.comparison_rules = ComparisonRulesContainer([
            ComparisonRule("osiedle", ComparisonRuleType.FORCE_CASE_INSENSITIVITY)
        ])

    def _extract_street_number(self, words_list, matched_location_slice_pos):
        _, slice_end = matched_location_slice_pos

        try:
            elem_after_slice = words_list[slice_end]
            street_number = int(elem_after_slice)
        except (IndexError, ValueError):
            return False, None
        else:
            return True, street_number

    def _get_comparator(self, location_name):
        if Tagger.Instance().does_contain_person_first_name(location_name):
            def name_equals(expected, actual):
                return NameComparator.equals(expected, actual,
                                             ignore_case_sensitivity_if_actual_is_all_upper_case=True)

            equality_comparator = name_equals
        else:
            def morphologic_equals(expected, actual):
                return MorphologicComparator.equals(expected, actual,
                                                    exception_rules=self.comparison_rules,
                                                    title_case_sensitive=True,
                                                    ignore_case_sensitivity_if_actual_is_all_upper_case=True)

            equality_comparator = morphologic_equals

        return equality_comparator

    def _match_locations(self, all_locations, description):
        all_matched_locations = []

        for location in all_locations:
            for location_name in [location["official"], *location["colloquial"]]:

                does_contain, (match_slice_pos, all_words) = TextSearcher.contains(
                    location_name,
                    description,
                    equality_comparator=self._get_comparator(location_name))

                if does_contain:
                    matched_location = location["official"]

                    success, street_number = self._extract_street_number(all_words, match_slice_pos)
                    if success:
                        matched_location += " " + str(street_number)

                    all_matched_locations.append(matched_location)

                    # noinspection PyUnreachableCode
                    if __debug__:
                        piece_of_text_that_matched = ' '.join(all_words[slice(*match_slice_pos)])
                        logging.debug(f"Matched {matched_location} = description:[{piece_of_text_that_matched}]")

        return all_matched_locations

    def __call__(self, description):
        """ Extracts location from description, returns (status, extracted_attribute_name, value) """
        matched_districts = self._match_locations(self.address_provider.districts, description)
        matched_estates = self._match_locations(self.address_provider.estates, description)
        matched_streets = self._match_locations(self.address_provider.streets, description)

        address = Address(district=matched_districts,
                          estate=matched_estates,
                          street=matched_streets)

        return bool(matched_districts or matched_estates or matched_streets), self.attribute_name, address
