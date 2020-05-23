import json
from collections import namedtuple

from exception import FlatFinderException
from src.singleton import Singleton

@Singleton
class AddressProvider:

    def __init__(self, city_name="Kraków"):
        data_dir = "../data/"

        with open(data_dir + "locations.json", encoding="UTF-8") as handle:
            json_locations = json.loads(handle.read())

        if city_name not in json_locations:
            raise FlatFinderException(f"Can't find locations for the '{city_name}' city. Pleas ensure it's available in database")

        locations = json_locations[city_name]["locations"]

        self._districts = locations["districts"]
        self._estates = locations["estates"]
        self._streets = locations["streets"]

    @property
    def districts(self):
        ''' Provides districts sorted by amount of words decreasing '''
        yield from self._districts

    @property
    def estates(self):
        ''' Provides estates sorted by amount of words decreasing'''
        yield from self._estates

    @property
    def streets(self):
        ''' Provides streets sorted by amount of words decreasing'''
        yield from self._streets
