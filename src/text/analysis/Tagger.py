from text.analysis.morphologic_analyser import MorphologicAnalyser
from decorators.singleton import Singleton
from env_utils.base_dir import base_dir


@Singleton
class Tagger:
    def __init__(self):
        self.first_names = {}
        with open(f"{base_dir}/data/first_names/polish.txt", encoding="utf8") as file_handle:
            self.first_names = set(data for data in file_handle.read().splitlines())

        self.contain_person_first_name_exceptions = {
            "aleja 3 maja": False}

    def does_contain_person_first_name(self, text):
        if text.lower().strip() in self.contain_person_first_name_exceptions:
            return self.contain_person_first_name_exceptions[text.lower().strip()]

        morf = MorphologicAnalyser.Instance()

        all_words = text.split()

        for word in all_words:
            for inflection in morf.get_base_form(word):
                if inflection in self.first_names:
                    return True

        return False
