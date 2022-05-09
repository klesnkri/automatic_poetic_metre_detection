import re
from typing import List


class SampaSyllableParser:
    """Class to parse token to X-SAMPA syllables using its X-SAMPA transcription."""

    # Regexps to find sonority peaks
    DIPHTONG_REGEX = r"(o_u|a_u|E_u)"
    VOWEL_REGEX = r"(I|E|a|o|u)"
    LONG_VOWEL_REGEX = r".:"
    SYLLABLE_CONSONANT_REGEX = r".="
    SONORITY_PEAKS_REGEXPS = [DIPHTONG_REGEX, SYLLABLE_CONSONANT_REGEX, LONG_VOWEL_REGEX, VOWEL_REGEX]

    def split_to_syllables(self, sampa_transcript: str) -> List[str]:
        """
        Split X-SAMPA transcription based on sonority peaks.
        For transcripts of non-syllabic tokens without sonority peaks the whole transcript is returned.
        :param sampa_transcript: X-SAMPA transcription
        :return: Split transcription
        """

        syllable_parts = []
        sonority_peaks = self._parse_sampa(sampa_transcript)

        for sonority_peak in sonority_peaks:
            idx = sampa_transcript.find(sonority_peak)
            syllable_parts.append(sampa_transcript[: idx + len(sonority_peak)])
            sampa_transcript = sampa_transcript[idx + len(sonority_peak) :]

        if len(sampa_transcript) > 0:
            if len(syllable_parts) > 0:
                syllable_parts[-1] += sampa_transcript
            else:
                syllable_parts.append(sampa_transcript)

        return syllable_parts

    def get_syllables(self, sampa_transcript: str) -> List[str]:
        """
        Get X-SAMPA syllables from X-SAMPA transcription.
        For transcripts of non-syllabic tokens without sonority peaks empty list is returned.
        :param sampa_transcript: X-SAMPA transcription
        :return: List of X-SAMPA syllables
        """
        syllable_cnt = self.get_syllable_cnt(sampa_transcript)
        return self.split_to_syllables(sampa_transcript) if syllable_cnt > 0 else []

    def get_syllable_cnt(self, sampa_transcript: str) -> int:
        """
        Get syllable cnt.
        For transcripts of non-syllabic tokens without sonority peaks 0 is returned.
        :param sampa_transcript: X-SAMPA transcription
        :return: Syllable cnt
        """
        return len(self._parse_sampa(sampa_transcript))

    def _parse_sampa(self, sampa_transcript: str) -> List[str]:
        """
        Parse X-SAMPA transcription to its sonority peaks.
        The lenght of the list is equal to the number of syllables.
        For transcripts of non-syllabic tokens without sonority peaks empty list is returned.
        :param sampa_transcript: X-SAMPA transcription
        :return: List of sonority peaks
        """
        sonority_peaks = []

        while len(sampa_transcript) > 0:
            sonority_peak = None

            for regex in self.SONORITY_PEAKS_REGEXPS:
                if match := re.match(regex, sampa_transcript):
                    sonority_peak = match.group()
                    break

            if sonority_peak:
                sonority_peaks.append(sonority_peak)
                sampa_transcript = sampa_transcript[len(sonority_peak) :]
            else:
                sampa_transcript = sampa_transcript[1:]

        return sonority_peaks

    def is_long_vowel(self, sonority_peak: str) -> bool:
        """
        Decide whether a given sonority peak represents a long vowel.
        :param sonority_peak: Sonority peak
        :return: Whether the syllable is long
        """
        return bool(re.match(self.LONG_VOWEL_REGEX, sonority_peak))

    def parse_line(self, line_data: List[dict]) -> list:
        """
        Parse line data to its sonority peaks.
        :param line_data: Line data
        :return: Parsed line
        """
        return [self._parse_sampa(word_data["xsampa"]) for word_data in line_data]

    def parse_poem(self, poem_data: list) -> list:
        """
        Parse poem data to its sonority peaks.
        :param poem_data: Poem data
        :return: Parsed poem
        """
        return [self.parse_line(line_data) for line_data in poem_data]

    def parse_poems(self, poems_data: list) -> list:
        """
        Parse poems data to its sonority peaks.
        :param poems_data: Poems data
        :return: Parsed poems
        """
        return [self.parse_poem(poem_data) for poem_data in poems_data]
