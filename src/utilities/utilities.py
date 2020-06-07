import functools
import re
from itertools import chain
from typing import List


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


def get_elements_before(*, idx, amount, the_list, ignored_values=[], fill_up=True, default=None): #TODO test
    all_elements_before = the_list[:idx]
    without_ignored = [e for e in all_elements_before if e not in ignored_values]

    n_elements_before = without_ignored[-amount:]

    if fill_up:
        filling = [default] * (amount - len(n_elements_before))
        n_elements_before = filling + n_elements_before

    return n_elements_before


def find_slice_beg(a_list, the_slice: List, *, find_all=False):
    if find_all:
        found = []
    else:
        found = None

    slice_len = len(the_slice)
    if slice_len > 0:
        for i in range(len(a_list)):
            if a_list[i:i+slice_len] == the_slice:
                if not find_all:
                    return i
                else:
                    found.append(i)

    return found


def neighbourhood(iterable):
    """yields tuple (previous, current, next) and sets previous and next to None if they're out of boundaries"""
    iterable = [None, *iterable, None]
    yield from zip(iterable, iterable[1:], iterable[2:])
