from dataclasses import dataclass


@dataclass
class StreetAddress:
    street_name: str
    unit_number: int = None

    def __str__(self):
        if self.unit_number is not None:
            return self.street_name + ' ' + str(self.unit_number)
        else:
            return self.street_name