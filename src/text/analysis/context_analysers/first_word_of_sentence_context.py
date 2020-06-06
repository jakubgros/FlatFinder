from containers.address_match import AddressMatch
from utilities.utilities import get_elements_before


class FirstWordOfSentenceContext:

    def __init__(self, negate=False):
        self.negate = negate

    def __call__(self, match: AddressMatch):
        subject_pos_beg, subject_pos_end = match.match_slice_position

        elements_before = get_elements_before(idx=subject_pos_beg, amount=2, the_list=match.source, ignored_values=['\n'])
        elements_before = [e.lower() if e else e for e in elements_before]

        abbreviations = {'ul', 'os', 'oś'}

        if elements_before[1] in ('.', None):
            ret = elements_before[0] not in abbreviations
        else:
            ret = False

        if self.negate:
            return not ret
        else:
            return ret

