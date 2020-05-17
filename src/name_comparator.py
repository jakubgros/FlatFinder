from nameparser import HumanName


from nameparser.config import CONSTANTS

from singleton import Singleton
from src.morfeusz import Morfeusz

@Singleton
class NameComparator:

    def __init__(self):
        CONSTANTS.titles.remove(*CONSTANTS.titles)

        morf = Morfeusz.Instance()

        with open("../data/name_titles/polish/titles.txt", encoding='UTF-8') as handle:
            for title in handle.read().splitlines():
                CONSTANTS.titles.add(title)
                CONSTANTS.first_name_titles.add(title)

                for title_synthesis in morf.morphological_synthesis(title):
                    CONSTANTS.titles.add(title_synthesis)
                    CONSTANTS.first_name_titles.add(title_synthesis)

    def _get_first_and_last(self, str_name):
        name = HumanName(str_name)

        first = name.first
        last = name.last

        # HumanName library doesn't recognize first and last name correctly if only one part was provided,
        # thus the correction is needed
        morf = Morfeusz.Instance()
        if not morf.does_contain_person_first_name(first):
            first, last = last, first

        return first, last

    def equals(self, lhs: str, rhs: str) -> bool:
        lhs_first, lhs_last = self._get_first_and_last(lhs)
        rhs_first, rhs_last = self._get_first_and_last(rhs)

        morf = Morfeusz.Instance()
        return (lhs_first == "" or rhs_first == "" or morf.equals(lhs_first, rhs_first))\
               and morf.equals(lhs_last, rhs_last)
