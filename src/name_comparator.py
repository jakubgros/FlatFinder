from nameparser import HumanName


from nameparser.config import CONSTANTS

from src.morfeusz import Morfeusz


class NameComparator:

    def __init__(self):
        CONSTANTS.titles.remove(*CONSTANTS.titles)

        morf = Morfeusz.Instance()
        with open("../data/name_titles/polish/titles.txt", encoding='UTF-8', ) as handle:
            for title in handle.read().splitlines():
                CONSTANTS.titles.add(title)
                for title_synthesis in morf.morphological_synthesis(title):
                    CONSTANTS.titles.add(title_synthesis)

    def equals(self, lhs, rhs):

        hn_lhs = HumanName(lhs)
        hn_rhs = HumanName(rhs)

        return hn_lhs.first == hn_rhs.first and hn_lhs.last == hn_rhs.last