from containers.street_address import StreetAddress
from parsers.address_extractor import AddressExtractor


class ExcludeAddressFilter:
    def __init__(self, excluded_addresses):
        self.excluded_addresses = excluded_addresses

    def __call__(self, flats):
        matching_filter = []

        for flat in flats:
            extracted_addresses = flat.description_extracted_attributes.get(AddressExtractor.attribute_name, set())
            extracted_address = [extracted_address.location for extracted_address in extracted_addresses.all_addresses]
            address_names = {address.street_name if isinstance(address, StreetAddress) else address for address in extracted_address}
            address_names.add(flat.address)

            if not address_names.intersection(self.excluded_addresses):
                matching_filter.append(flat)

        return matching_filter
