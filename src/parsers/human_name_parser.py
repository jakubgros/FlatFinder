from collections import namedtuple

from containers.morphologic_set import MorphologicSet
from decorators.singleton import Singleton
from env_utils.base_dir import base_dir
from parsers.roman_numerals_parser import RomanNumeralsParser
from utilities.utilities import split_on_special_characters
from dataclasses import dataclass, field
from typing import List


@dataclass
class HumanName:
    title: List[str] = field(default_factory=list)
    first_name: List[str] = field(default_factory=list)
    last_name: List[str] = field(default_factory=list)
    numerical_epithet: List[str] = field(default_factory=list)


@Singleton
class HumanNameParser:
    def __init__(self):
        self._all_valid_titles = MorphologicSet(self._load_data(f"{base_dir}/data/name_titles/polish/titles.txt"))
        self._all_valid_first_names = MorphologicSet(self._load_data(f"{base_dir}/data/first_names/polish.txt"))

    @staticmethod
    def _load_data(file_path):
        with open(file_path, encoding='UTF-8') as handle:
            loaded_data = [data for data in handle.read().splitlines()]

        return loaded_data

    def parse(self, name):
        name = split_on_special_characters(name)

        human_name = HumanName()

        word_it = iter(name)
        try:
            word = next(word_it)

            # titles
            while True:
                if word in self._all_valid_titles:
                    human_name.title.append(word)
                    word = next(word_it)
                else:
                    break

            # first names
            while True:
                if word in self._all_valid_first_names:
                    human_name.first_name.append(word)
                    word = next(word_it)
                else:
                    break

            # the rest is parsed as last_name or numerical epithet
            while True:
                if RomanNumeralsParser.is_roman_number(word):
                    human_name.numerical_epithet.append(word)
                else:
                    human_name.last_name.append(word)

                word = next(word_it)

        except StopIteration:
            pass

        return human_name
