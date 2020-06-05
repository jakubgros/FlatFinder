from containers.address_match import AddressMatch


def get_elements_before_ignoring_newline(idx, amount, the_list, default):
    sliced = the_list[:idx]
    without_newline = [e for e in sliced if e != '\n']
    reversed_slice = without_newline[::-1]

    elements_before = reversed_slice[:amount]

    return elements_before


class Context:

    @staticmethod
    def does_apply(context, subject):
        pass


class FirstWordOfSentenceContext(Context):

    def __init__(self, negate=False):
        self.negate = negate

    def __call__(self, match: AddressMatch):
        subject_pos_beg, subject_pos_end = match.match_slice_position

        elements_before = get_elements_before_ignoring_newline(subject_pos_beg, 2, match.source, None)
        elements_before = [e.lower() for e in elements_before]
        elements_before.extend([None] * (2 - len(elements_before))) # fill up to have length 2

        abbreviations = {'ul', 'os', 'oś'}

        if elements_before[0] in ('.', None):
            ret = elements_before[1] not in abbreviations
        else:
            ret = False

        if self.negate:
            return not ret
        else:
            return ret

        # TODO tomorrow fix test_address_extractor and test_context_analyser
        # polaczyc regression test z regression_extra_matches, bo context filtry moga wywalac dobre rzeczy
        # wywalic failujace testy z aktualnego regression zeby nie bylo tego smietnika z wylaczaniem testow
        # dodac extra matches counter do regression

