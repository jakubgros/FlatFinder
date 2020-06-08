from typing import Union, List

from text.text_frame import TextFrame
from utilities.utilities import split_on_special_characters


class TextSearcher:

    @staticmethod
    def find(
            *,
            phrase_to_find,
            text: Union[List[str], str],
            equality_comparator=lambda lhs, rhs: lhs == rhs):

        if isinstance(text, str):
            word_list = split_on_special_characters(text, preserve_special_characters=True)
        else:
            word_list = text

        max_frame_size = len(phrase_to_find.split())
        all_text_frames = (TextFrame(word_list, frame_size) for frame_size in range(1, max_frame_size + 1))

        for text_frame in all_text_frames:
            for slice_position, frame in text_frame:
                if equality_comparator(phrase_to_find, frame):
                    return True, (slice_position, text_frame.all_words)
        return False, (None, text_frame.all_words)
