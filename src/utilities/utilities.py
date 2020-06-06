import functools
import re


@functools.lru_cache(maxsize=10000)
def _split_on_special_characters_and_preserve(text, ignore_spaces):
    text_split = re.split('(\W)', text)
    if ignore_spaces:
        text_split = [word for word in text_split if word and word != ' ']

    return text_split


@functools.lru_cache(maxsize=10000)
def split_on_special_characters(text, *, preserve_special_characters=False, ignore_spaces=True):
    text_split = _split_on_special_characters_and_preserve(text, ignore_spaces)

    if not preserve_special_characters:
        text_split = [word for word in text_split if word.isalnum()]

    return text_split


def get_elements_before(*, idx, amount, the_list, ignored_values=[], fill_up=True, default=None):
    all_elements_before = the_list[:idx]
    without_ignored = [e for e in all_elements_before if e not in ignored_values]

    n_elements_before = without_ignored[-amount:]

    if fill_up:
        filling = [default] * (amount - len(n_elements_before))
        n_elements_before = filling + n_elements_before

    return n_elements_before

