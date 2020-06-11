import functools
import re
from typing import List

from env_utils.config import config


@functools.lru_cache(maxsize=config["cache_size"])
def _split_on_special_characters_and_preserve(text, ignore_spaces):
    text_split = re.split('(\W)', text)
    if ignore_spaces:
        text_split = [word for word in text_split if word and word != ' ']

    return text_split


@functools.lru_cache(maxsize=config["cache_size"])
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


def find_slice_beg(source, *, slice_to_find: List, find_all=False, case_insensitive=False):
    if find_all:
        found = []
    else:
        found = None

    slice_len = len(slice_to_find)
    if slice_len > 0:
        for i in range(len(source)):
            lhs = source[i:i + slice_len]
            rhs = slice_to_find

            if case_insensitive:
                lhs = [e.lower() for e in lhs]
                rhs = [e.lower() for e in rhs]

            if lhs == rhs:
                if not find_all:
                    return i
                else:
                    found.append(i)

    return found


def do_slices_overlap(lhs, rhs):
    ordered = [lhs, rhs]
    ordered.sort()

    first_beg, first_end = ordered[0]
    latter_beg, latter_end = ordered[1]

    if first_beg == first_end or latter_beg == latter_end:
        return False
    else:
        return first_end > latter_beg


def slice_span(a_slice):
    beg, end = a_slice
    return end - beg


def strip_list(the_list, *, strip_if_in):

    beg = 0
    for elem in the_list:
        if elem in strip_if_in:
            beg += 1
        else:
            break

    end = len(the_list)
    for elem in reversed(the_list):
        if elem in strip_if_in:
            end -= 1
        else:
            break

    if beg < end:
        return the_list[beg:end]
    else:
        return []
