import functools
import re

from containers.morphologic_set import MorphologicSet
from decorators.singleton import Singleton
from env_utils.base_dir import base_dir
from utilities.utilities import split_on_special_characters_and_preserve_them


@Singleton
class HumanNameParser:
    def __init__(self):
        self._all_valid_titles = MorphologicSet(self._load_data(f"{base_dir}/data/name_titles/polish/titles.txt"))
        self._all_valid_given_names = MorphologicSet(self._load_data(f"{base_dir}/data/first_names/polish.txt"))

    def _load_data(self, file_path):
        with open(file_path, encoding='UTF-8') as handle:
            loaded_data = [data for data in handle.read().splitlines()]

        return loaded_data

    def parse(self, name):
        name = [word for word in split_on_special_characters_and_preserve_them(name) if word.isalpha()]

        title = list()
        given_name = list()
        surname = list()

        word_it = iter(name)
        try:
            word = next(word_it)

            #titles
            while True:
                if word in self._all_valid_titles:
                    title.append(word)
                    word = next(word_it)
                else:
                    break

            #given names
            while True:
                if word in self._all_valid_given_names:
                    given_name.append(word)
                    word = next(word_it)
                else:
                    break

            #the rest is parsed as surname
            while True:
                surname.append(word)
                word = next(word_it)

        except StopIteration:
            pass

        return title, given_name, surname





