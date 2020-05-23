from functools import update_wrapper
from itertools import chain


class Singleton:
    def __init__(self, cls):
        self._cls = cls
        self._instances = dict()
        update_wrapper(self, cls)

    def Instance(self, *args, **kwargs):
        args_hash = [hash(arg) for arg in args]
        sorted_kwargs = dict(sorted(kwargs.items()))
        kwargs_hash = [hash(kwarg) for kwarg in sorted_kwargs]
        hash_key = ", ".join(str(e) for e in chain(args_hash, kwargs_hash))

        try:
            return self._instances[hash_key]
        except KeyError:
            self._instances[hash_key] = self._cls(*args, **kwargs)
            return self._instances[hash_key]

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)
