from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class AddressMatch:
    match_slice_position: Tuple[int, int]
    location: str
    source: List[str]

    @property
    def matched_phrase(self):
        return ' '.join(self.source[slice(*self.match_slice_position)])
