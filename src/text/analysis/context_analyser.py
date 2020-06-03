from containers.address_match import AddressMatch


def _safe_list_get(the_list, idx, default):
    if idx < 0:
        return default

    try:
        return the_list[idx]
    except IndexError:
        return default


class Context:
    @staticmethod
    def does_apply(context, subject):
        pass


class ContextNotFirstWordOfSentence(Context):
    @staticmethod
    def does_apply(match: AddressMatch):
        subject_pos_beg, subject_pos_end = match.match_slice_position

        elem_one_before = _safe_list_get(match.source, subject_pos_beg - 1, None)
        elem_two_before = _safe_list_get(match.source, subject_pos_beg - 2, None)

        if elem_one_before == '.':
            return False
        else:
            return [elem_two_before, elem_one_before] not in ([None, None], [None, '\n'], ['.', '\n'])
