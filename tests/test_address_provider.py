import unittest

from data_provider.address_provider import address_provider


class TestAddressProvider(unittest.TestCase):

    def test_provider(self):
        provider = address_provider
        self.assertTrue(len(provider.districts) != 0)
        self.assertTrue(len(provider.estates) != 0)
        self.assertTrue(len(provider.streets) != 0)

if __name__ == '__main__':
    unittest.main()
