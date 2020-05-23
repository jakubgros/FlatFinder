import functools
import re

from env_utils.base_dir import base_dir
from exception.exception import FFE_InvalidArgument
from decorators.singleton import Singleton


@Singleton
class MorphologicAnalyser:
    """ The used Morfeusz library doesn't have any synchronisation mechanisms so it's not safe to use it in multi-threaded environment
    straightaway - see Morfeusz's documentation how to handle it"""

    def __init__(self):
        import morfeusz2
        self.morf = morfeusz2.Morfeusz(dict_path=f'{base_dir}/third parties/morfeusz2-dictionary-polimorf',
                                       dict_name="polimorf")

        """ flection:
            mianownik (kto? co?)
            dopełniacz (kogo? czego?)
            celownik (komu? czemu?)
            biernik (kogo? co?)
            narzędnik ((z) kim? (z) czym?)
            miejscownik (o kim? o czym?)
            wołacz (o!).
        """
        #  for easier reading the data is provided in inverted form (lemma to list of flection)
        self._internal_lemma_dict = self._invert_dict({
            "Bonerowska": ("Bonerowska", "Bonerowskiej", "Bonerowskiej", "Bonerowską", "Bonerowską", "Bonerowskiej", "Bonerowsko"),
        })

        self._reinterpret_mapping = self._invert_dict({
            "osiedle": ("oś", "os")
        }, no_duplicates=True)

    def _invert_dict(self, dictionary, *, no_duplicates=False):
        inv_map = {}
        for key, values in dictionary.items():
            for v in values:
                if no_duplicates:
                    assert v not in inv_map
                    inv_map[v] = key
                else:
                    inv_map.setdefault(v, set()).add(key)
        return inv_map

    @functools.lru_cache(maxsize=10000)
    def get_inflection(self, val):  # TODO it's probably lemma - learn and rename
        """ To improve performance of cache, value passed to the function has to be a single word. If you have a sentence
        you have to call the function many times """
        if len(val.split()) > 1:
            raise FFE_InvalidArgument("Passed multi-word argument. The function accepts only single word as argument.")

        if val in self._reinterpret_mapping:
            val = self._reinterpret_mapping[val]

        inflection = set(base_form for _, _, (_, base_form, *_) in self.morf.analyse(val))
        assert inflection

        extension = self._internal_lemma_dict.get(val, set())
        inflection.update(extension)

        return inflection

    def morphological_synthesis(self, word):
        return [elem[0] for elem in self.morf.generate(word)]
