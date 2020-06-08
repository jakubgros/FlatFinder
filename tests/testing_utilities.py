from data_provider.address_provider import AddressProvider


class MockedAddressProvider(AddressProvider):
    def __init__(self, districts=[], estates=[], streets=[], places=[]):
        self.districts = districts
        self.estates = estates
        self.streets = streets
        self.places = places
