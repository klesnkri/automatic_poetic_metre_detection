from dataclasses import dataclass
from typing import Optional, List

from src.kveta.sampa_syllable_parser import SampaSyllableParser


@dataclass(unsafe_hash=True)
class SyllableClass:
    """Syllable class representation."""

    initial: bool
    final: bool
    content_word: Optional[bool]
    mpp_preposition: bool
    prev_mpp_preposition: bool
    prev_initial: Optional[bool]
    next_long: Optional[bool]

    def __init__(
        self, initial: bool, final: bool, content_word: bool, mpp_preposition: bool, prev_mpp_preposition: bool, prev_initial: bool, next_long: bool
    ) -> None:
        """
        :param initial: Is initial syllable
        :param final: Is final syllable
        :param content_word: Is inside content word
        :param mpp_preposition: Is MPP preposition
        :param prev_mpp_preposition: Previous syllable is MPP preposition
        :param prev_initial: Previous syllable is initial syllable
        :param next_long: Next syllable is long
        """
        # Reductions
        if initial and final and not prev_mpp_preposition:
            self.content_word = content_word
        else:
            self.content_word = None

        if (initial and not final) or mpp_preposition:
            self.prev_initial = prev_initial
            self.next_long = next_long
        else:
            self.prev_initial = None
            self.next_long = None

        # Assignment
        self.initial = initial
        self.final = final
        self.mpp_preposition = mpp_preposition
        self.prev_mpp_preposition = prev_mpp_preposition


class SyllableClassParser:
    """Class to obtain Syllable class for a syllable."""

    # POS tags
    NOUN_POS = "N"
    ADJECTIVE_POS = "A"
    NUMERAL_POS = "C"
    VERB_POS = "V"
    PREPOSITION_POS = "R"
    INTERJECTION_POS = "I"

    # MPP prepositions
    MPP_PREPOSITIONS = {"před", "od", "ob", "ku", "ke", "do", "ve", "po", "nad", "přes", "při", "bez", "se", "ze", "za", ", pod", "pro", "zpod"}

    def __init__(self) -> None:
        self.sampa_syll_parser = SampaSyllableParser()

    @staticmethod
    def _get_pos(morph_tag: str) -> str:
        """
        Extract POS tag from a morphological tag (Prague positional system).
        :param morph_tag: Morphological tag
        :return: POS tag
        """
        return morph_tag[0]

    def _is_content_word(self, morph_tag: str, lemma: str) -> bool:
        """
        Test whether a token represents a content word.
        :param morph_tag: Morphological tag of the token
        :param lemma: Lemma of the token
        :return: Whether the token represents a content word
        """
        pos = self._get_pos(morph_tag)
        return (pos in {self.NOUN_POS, self.ADJECTIVE_POS, self.NUMERAL_POS, self.INTERJECTION_POS}) or (pos == self.VERB_POS and lemma != "být")

    def _is_mpp_preposition(self, token: str, morph_tag: str) -> bool:
        """
        Test whether a token represents an MPP preposition.
        :param token: Token
        :param morph_tag: Morphological tag of the token
        :return: Whether the token represents an MPP preposition.
        """
        pos = self._get_pos(morph_tag)
        return pos == self.PREPOSITION_POS and token in self.MPP_PREPOSITIONS

    def _parse_token(
        self,
        token_sonority_peaks: List[str],
        token_data: dict,
        prev_token_sonority_peaks: Optional[List[str]],
        prev_token_data: Optional[dict],
        next_token_sonority_peaks: Optional[List[str]],
    ) -> List[SyllableClass]:
        """
        Parse token to its Syllable classes.
        :param token_sonority_peaks: Sonority peaks of the token syllables
        :param token_data: Data of the token
        :param prev_token_sonority_peaks: Sonority peaks of the previous token syllables, None for the first token in a line
        :param prev_token_data: Data of the previous token, None for the first token in a line
        :param next_token_sonority_peaks: Sonority peaks of the next token syllables, None for the last token in a line
        :return: Syllable classes of the token
        """
        syllable_classes = []

        content_word = self._is_content_word(token_data["morph"], token_data["lemma"])
        mpp_preposition = self._is_mpp_preposition(token_data["token_lc"], token_data["morph"])

        if prev_token_data:
            prev_mpp_preposition = self._is_mpp_preposition(prev_token_data["token_lc"], prev_token_data["morph"])
            prev_initial = len(prev_token_sonority_peaks) == 1
        else:
            prev_mpp_preposition = False
            prev_initial = False

        # 2 subsequent MPP prepositions
        if mpp_preposition and prev_mpp_preposition:
            mpp_preposition = False

        for idx, _ in enumerate(token_sonority_peaks):
            initial = idx == 0
            final = idx == len(token_sonority_peaks) - 1

            if idx < len(token_sonority_peaks) - 1:
                next_long = self.sampa_syll_parser.is_long_vowel(token_sonority_peaks[idx + 1])
            elif next_token_sonority_peaks:
                next_long = self.sampa_syll_parser.is_long_vowel(next_token_sonority_peaks[0])
            else:
                next_long = False

            syllable_classes.append(SyllableClass(initial, final, content_word, mpp_preposition, prev_mpp_preposition, prev_initial, next_long))

            if prev_mpp_preposition:
                prev_mpp_preposition = False

            prev_initial = idx == 0

        return syllable_classes

    def parse_line(self, line_sonority_peaks: list, line_data: List[dict]) -> list:
        """
        Parse line to its Syllable classes.
        :param line_sonority_peaks: Sonority peaks of the line syllables
        :param line_data: Data of the line
        :return: Syllable classes of the line
        """
        syllables_classes = []

        prev_token_sonority_peaks = None
        prev_token_data = None

        for idx, (token_sonority_peaks, token_data) in enumerate(zip(line_sonority_peaks, line_data)):
            if idx == len(line_sonority_peaks) - 1:
                next_token_sonority_peaks = None
            else:
                next_token_sonority_peaks = line_sonority_peaks[idx + 1]

            syllables_classes.append(self._parse_token(token_sonority_peaks, token_data, prev_token_sonority_peaks, prev_token_data, next_token_sonority_peaks))

            prev_token_sonority_peaks = token_sonority_peaks
            prev_token_data = token_data

        return syllables_classes

    def parse_poem(self, poem_sonority_peaks: list, poem_data: list) -> list:
        """
        Parse poem to its Syllable classes.
        :param poem_sonority_peaks: Sonority peaks of the poem syllables
        :param poem_data: Data of the poem
        :return: Syllable classes of the poem
        """
        return [self.parse_line(line_sonority_peaks, line_data) for (line_sonority_peaks, line_data) in zip(poem_sonority_peaks, poem_data)]

    def parse_poems(self, poems_sonority_peaks: list, poems_data: list) -> list:
        """
        Parse poems to its Syllable classes.
        :param poems_sonority_peaks: Sonority peaks of the poems syllables
        :param poems_data: Data of the poems
        :return: Syllable classes of the poems
        """
        return [self.parse_poem(poem_sonority_peaks, poem_data) for (poem_sonority_peaks, poem_data) in zip(poems_sonority_peaks, poems_data)]
