class AttributeFilter:
    def __init__(self, name, accepted_values):
        self.name = name
        self.accepted_values = accepted_values

    def __call__(self, flat):
        attribute_val = flat.extract_info_from_description.get(self.name, set())
        return attribute_val.intersection(self.accepted_values)
