import json
import os
from pprint import pprint
import uuid

from env_utils.base_dir import base_dir
from other.EmailSender import EmailSender
from os import listdir
from os.path import isfile, join

class Database:
    def __init__(self):
        self.amount_of_all_processed = 0
        self.currently_printed_id = 0
        self._processed_flats_by_titles = {}
        self.saved_links = set()

        self._parsed_flats_dir = f"{base_dir}/data/database/parsed_flats"

        self._load_db_from_disc()

        self._email_sender = EmailSender()

    def _load_db_from_disc(self):
        flat_files = [join(self._parsed_flats_dir, file) for file in listdir(self._parsed_flats_dir)
                      if isfile(join(self._parsed_flats_dir, file))]

        for flat_file in flat_files:
            with open(flat_file, "r") as in_handle:
                flat = json.load(in_handle)
                self._processed_flats_by_titles[flat['title']] = flat

        try:
            with open(f"{self._parsed_flats_dir}/../processed_links.txt", "r") as in_handle:
                for link in in_handle.read().splitlines():
                    self.saved_links.add(link)
        except FileNotFoundError:
            pass

    def _save_to_disc(self, flat):
        while True:
            file_name = str(uuid.uuid4()) + ".json"
            file_path = f"{self._parsed_flats_dir}/{file_name}"
            if not os.path.exists(file_path):
                break

        with open(file_path, "w") as out_handle:
            json.dump(flat.to_dict(), out_handle, indent=2)

    def save_flat(self, flat, filters):
        #not filtered output
        self._processed_flats_by_titles[flat.title] = flat
        self._save_to_disc(flat)

        #filtered output
        flats = [flat]
        for filters in filters:
            flats = filters(flats)


        for flat in flats:
            self.currently_printed_id += 1
            self._save_to_email(flat)
            self._save_to_console(flat)

    def _save_to_console(self, flat):
        print(f"[{self.currently_printed_id}/{self.amount_of_all_processed}]")
        pprint(flat.to_dict(), indent=2)

    def _save_to_email(self, flat):
        self._email_sender.send(flat)

    def save_link(self, link):
        with open(f"{self._parsed_flats_dir}/../processed_links.txt", "a") as out_handle:
            print(link, file=out_handle)

        self.saved_links.add(link)

    def has_link(self, link):
        return link in self.saved_links

    def has_flat(self, flat):
        return flat.title in self._processed_flats_by_titles

    def increase_processed_flats_counter(self):
        self.amount_of_all_processed += 1

