class AttributeFilter:
    def __init__(self, name, accepted_values):
        self.name = name
        self.accepted_values = accepted_values

    def __call__(self, flats):
        matching_filter = []

        for flat in flats:
            attribute_val = flat.description_extracted_attributes.get(self.name, set())
            if attribute_val.intersection(self.accepted_values):
                matching_filter.append(flat)

        return matching_filter
