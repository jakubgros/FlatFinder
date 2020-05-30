import functools
from typing import Tuple, Dict

import morfeusz2

from decorators.singleton import Singleton
from env_utils.base_dir import base_dir
from exception.exception import FFE_InvalidArgument


@Singleton
class MorphologicAnalyser:
    """ The used Morfeusz library doesn't have any synchronisation mechanisms, so it's not safe
    to use it in multi-thread environment straightaway - see Morfeusz's documentation how to workaround it """

    def __init__(self):
        self._morf = morfeusz2.Morfeusz(dict_path=f'{base_dir}/third parties/morfeusz2-dictionary-polimorf',
                                        dict_name="polimorf")

        self._base_form_extension = None
        self.reset_base_form_extension()

        self._base_form_removals = None
        self.reset_base_form_removals()

        self._reinterpret_mapping = None
        self.reset_reinterpret_mapping()

    def reset_base_form_removals(self, value: Dict[str, Tuple[str]] = None):
        self.get_base_form.cache_clear()

        if value is None:
            self._base_form_removals = {
                "Kraków": ("Krak", "Kraka"),
            }
        else:
            self._base_form_removals = value

    def reset_base_form_extension(self, value: Dict[str, Tuple[str]] = None):
        self.get_base_form.cache_clear()

        if value is None:
            self._base_form_extension = self._invert_dict({
            "Bonerowska": ("Bonerowska", "Bonerowskiej", "Bonerowskiej",
                           "Bonerowską", "Bonerowską", "Bonerowskiej", "Bonerowsko"),
            })
        else:
            self._base_form_extension = self._invert_dict(value)

    def reset_reinterpret_mapping(self, value: Dict[str, Tuple[str]] = None):
        """ The dictionary cannot contain any value repetition, even if it's assigned to different key """
        self.get_base_form.cache_clear()

        if value is None:
            self._reinterpret_mapping = self._invert_dict({
                "osiedle": ("oś", "os")
            }, no_duplicates=True)
        else:
            self._reinterpret_mapping = self._invert_dict(value, no_duplicates=True)

    @functools.lru_cache(maxsize=10000)
    def get_base_form(self, str_val):
        """ Returns base form for a given word. To improve cache hits, value passed to the function has to
        be a single word. If you have a sentence you have to call the function many times """

        if len(str_val.split()) > 1:
            raise FFE_InvalidArgument("Passed multi-word argument. The function accepts only single word as argument.")

        if str_val in self._reinterpret_mapping:
            str_val = self._reinterpret_mapping[str_val]

        base_form = set(base_form for _, _, (_, base_form, *_) in self._morf.analyse(str_val))
        assert base_form

        extension = self._base_form_extension.get(str_val, set())
        base_form.update(extension)

        removals = self._base_form_removals.get(str_val, set())
        base_form = base_form.difference(removals)

        return base_form

    @staticmethod
    def _invert_dict(dictionary, *, no_duplicates=False):
        inv_map = {}
        for key, values in dictionary.items():
            for v in values:
                if no_duplicates:

                    if v in inv_map:
                        raise FFE_InvalidArgument("Provided dictionary cannot be converted without value duplicates")

                    inv_map[v] = key
                else:
                    inv_map.setdefault(v, set()).add(key)
        return inv_map
