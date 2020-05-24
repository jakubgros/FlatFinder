import functools
import re


@functools.lru_cache(maxsize=10000)
def split_on_special_characters_and_preserve_them(text):
    split_text = re.split('\(|\)| |-|,|\.|\n', text)

    text_split = re.split('(\+|\(|\)| |-|:|;|!|,|\.|\n)', text)
    text_split = [word.strip() for word in text_split if word and word.strip()]

    return text_split
