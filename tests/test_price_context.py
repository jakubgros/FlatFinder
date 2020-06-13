import unittest

from containers.address_match import AddressMatch
from text.analysis.context_analysers.price_context import PriceContext


class TestPriceContext(unittest.TestCase):

    def test_context(self):
        ctx_analyser = PriceContext()

        match = AddressMatch(
            match_slice_position=(1, 2),
            location='', #  doesn't matter
            source=['500', 'zł'],
        )

        self.assertTrue(ctx_analyser(match))

        match = AddressMatch(
            match_slice_position=(1, 2),
            location='', #  doesn't matter
            source=['okolica', 'złotych', 'tarasów'],
        )
        self.assertFalse(ctx_analyser(match))

if __name__ == '__main__':
    unittest.main()
