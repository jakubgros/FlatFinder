class MockedAddressProvider:
    def __init__(self, districts=[], estates=[], streets=[]):
        self.districts = districts
        self.estates = estates
        self.streets = streets
