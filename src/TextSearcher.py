from text_frame import TextFrame


class TextSearcher:

    @staticmethod
    def contains(phrase, text, *,
                 exception_rules=None,
                 title_case_sensitive=False,
                 equality_comparator=lambda lhs, rhs: lhs == rhs):
        frame_size = min(len(phrase.split()), len(text.split()))

        text_frame = TextFrame(text, frame_size)
        for slice_position, frame in text_frame:
            if equality_comparator(phrase, frame):
                return True, (slice_position, text_frame.all_words)

        return False, (None, text_frame.all_words)