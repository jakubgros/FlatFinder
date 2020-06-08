import json

from env_utils.base_dir import base_dir
from exception.exception import FlatFinderException

class AddressProvider:

    def __init__(self, city_name="Kraków"):
        with open(f"{base_dir}/data/locations.json", encoding="UTF-8") as handle:
            json_locations = json.loads(handle.read())

        if city_name not in json_locations:
            raise FlatFinderException(f"Can't find locations for the '{city_name}' city."
                                      f" Pleas ensure it's available in database")

        locations = json_locations[city_name]["locations"]

        self.districts = locations["districts"]
        self.estates = locations["estates"]
        self.streets = locations["streets"]
        self.places = locations["places"]


address_provider = AddressProvider()
