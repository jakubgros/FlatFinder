from functools import update_wrapper

class Singleton:

    def __init__(self, cls):
        self._cls = cls
        update_wrapper(self, cls)

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)
