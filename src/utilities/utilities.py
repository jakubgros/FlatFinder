import functools
import re


@functools.lru_cache(maxsize=10000)
def _split_on_special_characters_and_preserve(text):
    split_text = re.split('\(|\)| |-|,|\.|\n', text)

    text_split = re.split('(\+|\(|\)| |-|:|;|!|,|\.|\n)', text)
    text_split = [word.strip() for word in text_split if word and word.strip()]

    return text_split


@functools.lru_cache(maxsize=10000)
def split_on_special_characters(text, *, preserve_special_characters=False):
    text_split = _split_on_special_characters_and_preserve(text)

    if not preserve_special_characters:
        text_split = [word for word in text_split if word.isalnum()]

    return text_split
