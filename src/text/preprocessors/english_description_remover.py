import re

import enchant

from utilities.utilities import split_on_special_characters


class EnglishDescriptionRemover:
    def __init__(self):
        self.english_dict = enchant.Dict("en_US")

    def _tag_words(self, split_text):
        is_english_word = []
        for word in split_text:
            is_english = self.english_dict.check(word)
            is_special_character = bool(re.match('\W', word))

            if is_special_character:
                tag = 'special character'
            elif is_english:
                tag = 'english word'
            else:
                tag = 'other'

            is_english_word.append((word, tag))

        return is_english_word

    def _get_biggest_english_part(self, split_text):
        tag_values = {
            'special character': -0.0000000001,
            'english word': 1,
            'other': -1
        }

        max_score = 0, (0, 0)
        split_text_tagged_english = self._tag_words(split_text)

        txt_len = len(split_text_tagged_english)
        for slice_end in range(txt_len+1):
            for slice_beg in range(slice_end):

                score = 0
                for _, tag in split_text_tagged_english[slice_beg:slice_end]:
                    score += tag_values[tag]

                max_val, *_ = max_score
                if score >= max_val:
                    max_score = score, (slice_beg, slice_end)

        _, (max_score_slice_beg, max_score_slice_end) = max_score
        return max_score_slice_beg, max_score_slice_end

    def process(self, text, min_snippet_remove_size=5):
        split_text = split_on_special_characters(text, preserve_special_characters=True, ignore_spaces=False)

        while True:
            slice_beg, slice_end = self._get_biggest_english_part(split_text)

            if slice_end - slice_beg < min_snippet_remove_size:
                return ''.join(split_text).strip()

            split_text = [word for index, word in enumerate(split_text) if index not in range(slice_beg, slice_end+1)]

