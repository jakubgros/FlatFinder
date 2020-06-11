from containers.morphologic_set import MorphologicSet
from env_utils.base_dir import base_dir
from exception.exception import FFE_InvalidArgument
from parsers.roman_numerals_parser import RomanNumeralsParser
from utilities.utilities import split_on_special_characters, strip_list
from dataclasses import dataclass, field
from typing import List


@dataclass
class HumanName:
    title: List[str] = field(default_factory=list)
    first_name: List[str] = field(default_factory=list)
    last_name: List[str] = field(default_factory=list)
    numerical_epithet: List[str] = field(default_factory=list)

    def to_list(self):
        return self.title + self.first_name + self.last_name + self.numerical_epithet

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
        name_split = split_on_special_characters(name)

        human_name = HumanName()

        word_it = iter(name_split)
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

        name_split_with_special_characters_preserved \
            = split_on_special_characters(name, preserve_special_characters=True)
        all_matched = human_name.to_list()
        has_matched = [elem in all_matched for elem in name_split_with_special_characters_preserved]
        stripped_has_matched = strip_list(has_matched, strip_if_in=[False])
        if len(has_matched) != len(stripped_has_matched):
            raise FFE_InvalidArgument("Provided string contains leading or trailing special characters")

        return human_name


human_name_parser = HumanNameParser()