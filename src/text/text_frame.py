class TextFrame:
    def __init__(self, word_list, frame_size):
        self.word_list = word_list
        self.frame_size = frame_size

    @property
    def all_words(self):
        return self.word_list

    def __iter__(self):
        words_count = len(self.word_list)

        if self.frame_size > words_count:
            return

        for start in range(words_count - self.frame_size + 1):
            end = start + self.frame_size
            yield (start, end), " ".join(self.word_list[start:end])
