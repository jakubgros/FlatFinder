from comparators.morphologic_comparator import MorphologicComparator
from decorators.singleton import Singleton
from env_utils.base_dir import base_dir
from text.text_searcher import TextSearcher
from text.analysis.morphologic_analyser import MorphologicAnalyser


@Singleton
class Tagger:
    def __init__(self):
        with open(f"{base_dir}/data/first_names/polish.txt", encoding="utf8") as file_handle:
            self._first_names = set(data for data in file_handle.read().splitlines())

        self._analyser = MorphologicAnalyser.Instance()

        self._contain_person_first_name_exceptions = None
        self.reset_contain_person_first_name_exceptions()

    def reset_contain_person_first_name_exceptions(self, contain_exceptions=None):
        if contain_exceptions is None:
            self._contain_person_first_name_exceptions = {
                "Aleja 3 Maja": False
            }
        else:
            self._contain_person_first_name_exceptions = contain_exceptions

    def does_contain_person_first_name(self, text):
        # check contain_exceptions
        for contain_exception, ret_val in self._contain_person_first_name_exceptions.items():
            comparator = MorphologicComparator().equals
            does_contain, *_ = TextSearcher.find(phrase_to_find=contain_exception,
                                                 text=text,
                                                 equality_comparator=comparator)
            if does_contain:
                return ret_val

        # do normal text analysis
        for word in text.split():
            for inflection in self._analyser.get_base_form(word):
                if inflection in self._first_names:
                    return True
        return False
