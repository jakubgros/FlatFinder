from collections import namedtuple

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

    def _match_locations(self, all_locations, description):
        matched_locations = []
        for location in all_locations:
            if self.morfeusz.contains(location, description,
                                      exception_rules=self.exception_rules,
                                      title_case_sensitive=True):
                matched_locations.append(location)

        return matched_locations

    def __call__(self, description):
        """ Extracts location from description, returns (status, extracted_attribute_name, value) """

        matched_districts = self._match_locations(self.address_provider.districts, description)
        matched_estates = self._match_locations(self.address_provider.estates, description)
        matched_streets = self._match_locations(self.address_provider.streets, description)

        address = Address(district=matched_districts,
                          estate=matched_estates,
                          street=matched_streets)

        return bool(matched_districts or matched_estates or matched_streets),\
            self.attribute_name,\
            address


'''
#TODO add context checking:
- don't match after dot
- don't match after newline (not sure)

Add extraction from title

'''