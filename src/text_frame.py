import re
class TextFrame:
    def __init__(self, text, frame_size):
        self.text = text
        self.frame_size = frame_size

        text_split = re.split('(\+|\(|\)| |-|:|;|!|,|\.|\n)', self.text)
        self.text_split = [word.strip() for word in text_split if word and word.strip()]

    @property
    def all_words(self):
        return self.text_split

    def __iter__(self):
        words_count = len(self.text_split)

        if self.frame_size > words_count:
            return

        for i in range(words_count - self.frame_size + 1):
            start = i
            end = start + self.frame_size
            yield ((start, end), " ".join(self.text_split[start:end]))
