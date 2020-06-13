from containers.address_match import AddressMatch
import re

from utilities.utilities import safe_list_get, is_float


class PriceContext:

    @staticmethod
    def _is_in_price_context(match):
        beg, _ = match.match_slice_position
        elem_before = safe_list_get(match.source, index=beg-1, default='')
        return is_float(elem_before)

    def __call__(self, match: AddressMatch):
        matched_phrase = match.matched_phrase.lower()

        currencies_found = [match.span() for match in re.finditer('zl|zł|złotych', matched_phrase)]

        if not currencies_found:
            return False
        else:
            return self._is_in_price_context(match)
