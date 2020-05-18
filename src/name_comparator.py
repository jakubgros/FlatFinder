from itertools import zip_longest

from Tagger import Tagger
from human_name_parser import HumanNameParser
from singleton import Singleton

from src.morfeusz import Morfeusz

class NameComparator:
    @staticmethod
    def equals(lhs: str, rhs: str) -> bool:
        name_parser = HumanNameParser.Instance()

        _, lhs_first, lhs_last = name_parser.parse(lhs)
        _, rhs_first, rhs_last = name_parser.parse(rhs)

        morf = Morfeusz.Instance()

        if (not lhs_first or not rhs_first) and (rhs_first or rhs_last):
            return all(morf.equals(*comp_pair) for comp_pair in zip_longest(lhs_last, rhs_last, fillvalue=""))
        else:
            return all(morf.equals(*comp_pair) for comp_pair in zip_longest(lhs_first, rhs_first, fillvalue="")) \
                   and all(morf.equals(*comp_pair) for comp_pair in zip_longest(lhs_last, rhs_last, fillvalue=""))
