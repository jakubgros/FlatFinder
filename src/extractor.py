import logging
from collections import namedtuple

from Tagger import Tagger
from name_comparator import NameComparator
from src.TextSearcher import TextSearcher
from src.exception_rule import ExceptionRule
from src.exception_rule_type import ExceptionRuleType

from src.exception_rules_container import ExceptionRulesContainer
from src.morfeusz import Morfeusz

Address = namedtuple('Address', ['district', 'estate', 'street'])


class AddressExtractor:
    def __init__(self, address_provider):
        self.address_provider = address_provider
        self.morfeusz = Morfeusz.Instance()
        self.attribute_name = "address"

        self.exception_rules = ExceptionRulesContainer([
            ExceptionRule("osiedle", ExceptionRuleType.FORCE_CASE_INSENTIVITIY)
        ])

    def _extract_street_number(self, all_words, matched_location_slice_pos):
        slice_start, slice_end = matched_location_slice_pos
        if len(all_words) < slice_end+1:
            return False, None

        elem_after_slice = all_words[slice_end]

        try:
            street_number = int(elem_after_slice)
            return True, street_number
        except ValueError:
            return False, None

    def _match_locations(self, all_locations, description):
        all_matched_locations = []
        for location in all_locations:
            if Tagger.Instance().does_contain_person_first_name(location):
                def name_equals(expected, actual):
                    return NameComparator.equals(expected, actual, ignore_case_sensitivity_if_actual_is_all_upper_case=True)
                equality_comparator = name_equals
            else:
                def morphologic_equals(expected, actual):
                    return self.morfeusz.equals(expected, actual, exception_rules=self.exception_rules, title_case_sensitive=True, ignore_case_sensitivity_if_actual_is_all_upper_case=True)
                equality_comparator = morphologic_equals

            does_contain, (matched_location_slice_pos, all_words) \
                = TextSearcher.contains(location, description, equality_comparator=equality_comparator)

            if does_contain:
                success, street_number = self._extract_street_number(all_words, matched_location_slice_pos)
                matched_location = location
                if success:
                    matched_location += " " + str(street_number)
                all_matched_locations.append(matched_location)
                slice_beg, slice_end = matched_location_slice_pos

                piece_of_text_that_matched = ' '.join(all_words[slice_beg:slice_end])
                logging.debug(f"Matched: db[{matched_location}] = text[{piece_of_text_that_matched}]")

        return all_matched_locations

    def __call__(self, description):
        """ Extracts location from description, returns (status, extracted_attribute_name, value) """
        matched_districts = self._match_locations(self.address_provider.districts, description)
        matched_estates = self._match_locations(self.address_provider.estates, description)
        matched_streets = self._match_locations(self.address_provider.streets, description)

        address = Address(district=matched_districts,
                          estate=matched_estates,
                          street=matched_streets)

        return bool(matched_districts or matched_estates or matched_streets), \
               self.attribute_name, \
               address


'''
#TODO add context checking:
- don't match after dot
- don't match after newline (not sure)

Add extraction from title

'''
