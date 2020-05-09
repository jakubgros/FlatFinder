from src.singleton import Singleton

@Singleton
class AddressProvider:

    def _loadData(self, file_path):
        loaded_data = []
        with open(file_path, encoding="utf8") as file_handle:
            for data in file_handle:
                loaded_data.append(data.rstrip('\n').strip())

        return loaded_data

    def __init__(self):
        data_dir = "../data/Cracow/"

        self._districts = self._loadData(data_dir + "districts.txt")
        self._districts.sort(key=lambda x: len(x.split()), reverse=True)

        self._estates = self._loadData(data_dir + "estates.txt")
        self._estates.sort(key=lambda x: len(x.split()), reverse=True)

        self._streets = self._loadData(data_dir + "streets.txt")
        self._streets.sort(key=lambda x: len(x.split()), reverse=True)

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
