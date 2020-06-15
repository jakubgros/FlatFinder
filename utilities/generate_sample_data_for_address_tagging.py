import json
from env_utils.base_dir import base_dir
from containers.flat import Flat
from data_provider.gumtree_flat_provider import GumtreeFlatProvider


def fetch_flat_announcements_and_save_to_json(*, save_dir, amount, start_index):
    provider = GumtreeFlatProvider()

    all_flats = {}
    announcements_it = provider.announcements
    i = start_index - 1
    while len(all_flats) < amount:
        url = next(announcements_it)
        i += 1

        print(i)

        try:
            flat = Flat.from_url(url)
        except Exception as e:
            print(e)
            continue

        if any(saved_flat['title'] == flat.title for saved_flat in all_flats.values()):
            continue

        all_flats[i] = {
            'title': flat.title,
            'url': flat.url,
            'locations': [],
            'description': flat.description,
        }

    parsed = json.dumps(all_flats, indent=2, ensure_ascii=False)

    with open(save_dir, "w", encoding="utf-8") as out_handle:
        print(parsed, file=out_handle)


if __name__ == "__main__":
    fetch_flat_announcements_and_save_to_json(
        amount=30,
        start_index=27,
        save_dir=f"{base_dir}/temp/flats.json")
