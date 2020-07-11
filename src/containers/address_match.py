from dataclasses import dataclass
from typing import Tuple, List, Any


@dataclass
class AddressMatch:
    match_slice_position: Tuple[int, int]
    location: Any
    source: List[str]

    @property
    def matched_phrase(self):
        return ' '.join(self.source[slice(*self.match_slice_position)])

    def __str__(self):
        return str(self.location)