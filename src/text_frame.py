import re
class TextFrame:
    def __init__(self, text, frame_size):
        self.text = text
        self.frame_size = frame_size

    def __iter__(self):
        text_split = re.split(' |-|:|;|!|,|\.|\n', self.text)
        text_split = [word.strip() for word in text_split if word.strip()]
        words_count = len(text_split)

        if self.frame_size > words_count:
            return

        for i in range(words_count - self.frame_size + 1):
            yield " ".join(text_split[i:i+self.frame_size])
