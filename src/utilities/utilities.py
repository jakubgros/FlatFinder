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
