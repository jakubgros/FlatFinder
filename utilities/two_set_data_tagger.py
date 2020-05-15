import os
import time
from collections import defaultdict
import keyboard




class TwoTypeDataTagger:
    def __init__(self, data_to_tag_dir, tagged_data_save_dir):
        self.tagged_data = defaultdict(list)
        self.data_dir = data_to_tag_dir
        self.tagged_data_save_dir = tagged_data_save_dir

    def raw_data(self):
        with open(self.data_dir, encoding='UTF-8') as handle:
            return handle.read().splitlines()

    def tag_data(self, tag, tagged_data):
        self.tagged_data[tag].append(tagged_data)

    def save_tagged_data(self):
        for key in self.tagged_data.keys():
            with open(f'{self.tagged_data_save_dir}/{key}.txt', 'w', encoding='UTF-8') as save_handle:
                for item in self.tagged_data[key]:
                    print(item, file=save_handle)

    def run(self):
        length = len(self.raw_data())

        for idx, data in enumerate(self.raw_data()):
            print(f'[{idx}/{length}]')
            print(data)
            if len(data.split()) == 1:
                tag = "a"
            else:
                tag = input()

            if tag == "save and quit":
                self.save_tagged_data()
                return

            self.tag_data(tag, data)

        self.save_tagged_data()



if __name__ == "__main__":

    tagger = TwoTypeDataTagger(data_to_tag_dir=r"C:\Users\jakub\Desktop\FlatFinder\temp\all_locations_to_tag.txt",
                               tagged_data_save_dir=r"C:\Users\jakub\Desktop\FlatFinder\temp")

    tagger.run()