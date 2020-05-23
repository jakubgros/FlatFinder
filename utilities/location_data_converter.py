import json


def convert_enter_separated_location_data_to_internal_representation(
        city,
        districts_input_file_path,
        estates_input_file_path,
        streets_input_file_path,
        output_file_path):
    """ converter from *.txt data representation where each entry is put in new line.
     The converter creates new internal representation, it doesn't append to current one.
     If output file already exists, it will be overriden"""

    json_data = {
        f"{city}": {
            "locations": {
                "districts": [],
                "estates": [],
                "streets": [],
            },
        },
    }

    with open(districts_input_file_path, encoding="utf-8") as in_handle:
        for in_data in in_handle.read().splitlines():
            json_data[f"{city}"]["locations"]["districts"].append({
                "official": f"{in_data}",
                "colloquial": [],
            })

    with open(estates_input_file_path, encoding="utf-8") as in_handle:
        for in_data in in_handle.read().splitlines():
            json_data[f"{city}"]["locations"]["estates"].append({
                "official": f"{in_data}",
                "colloquial": [],
            })

    with open(streets_input_file_path, encoding="utf-8") as in_handle:
        for in_data in in_handle.read().splitlines():
            json_data[f"{city}"]["locations"]["streets"].append({
                "official": f"{in_data}",
                "colloquial": [],
            })

    parsed = json.dumps(json_data, indent=4, ensure_ascii=False)

    with open(output_file_path, "w", encoding="utf-8") as out_handle:
        print(parsed, file=out_handle)


if __name__ == "__main__":
    convert_enter_separated_location_data_to_internal_representation(
        city="Kraków",
        districts_input_file_path=r"C:\Users\jakub\Desktop\FlatFinder\temp\districts.txt",
        estates_input_file_path=r"C:\Users\jakub\Desktop\FlatFinder\temp\estates.txt",
        streets_input_file_path=r"C:\Users\jakub\Desktop\FlatFinder\temp\streets.txt",
        output_file_path=r"C:\Users\jakub\Desktop\FlatFinder\temp\internal.json",
    )
