from morfeusz import Morfeusz
from singleton import Singleton


@Singleton
class Tagger:
    def __init__(self):
        self.first_names = {}
        with open("../data/first_names/polish.txt", encoding="utf8") as file_handle:
            for data in file_handle.read().splitlines():
                self.first_names[data] = True

    def does_contain_person_first_name(self, text):
        morf = Morfeusz.Instance()

        all_words = text.split()

        for word in all_words:
            for inflection in morf.get_inflection(word):
                if inflection in self.first_names:
                    return True

        return False
