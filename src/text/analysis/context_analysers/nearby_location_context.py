from containers.address_match import AddressMatch
from utilities.utilities import get_elements_before, split_on_special_characters


class NearbyLocationContext:
    def __init__(self, negate=False):
        self.negate = negate

    def __call__(self, match: AddressMatch):
        subject_pos_beg, subject_pos_end = match.match_slice_position

        nearby_location_introducers = {'w sąsiedztwie'}

        ret = False

        for introducer in nearby_location_introducers:
            introducer = split_on_special_characters(introducer, preserve_special_characters=True)

            elements_before = get_elements_before(idx=subject_pos_beg, amount=len(introducer), the_list=match.source,
                                                  ignored_values=['\n'])

            if elements_before == introducer:
                ret = True
                break


        if self.negate:
            return not ret
        else:
            return ret

