import re
from itertools import product
from typing import Optional, Tuple, Callable, Iterable, List


class MetreGenerator:
    """Class to generate all possible metres for a poem based on its syllable counts."""

    # Regex of a valid Czech syllabotonic line metrical pattern
    SYLLABOTONIC_REGEX = re.compile(r"^W?(SWW?)*(SW?)?$")

    # All possible metrical positions
    METRICAL_POSITIONS = "SW"

    # Poem metrical patterns of quantitative syllabic strophes
    QUANTITATIVE_SYLLABIC_STROPHES_PATTERNS = {
        "sapphic": [
            "SWSWSWWSWSW",
            "SWSWSWWSWSW",
            "SWSWSWWSWSW",
            "SWWSW",
        ],
        "asclepiad": [
            "SWSWWSWSWWSWW",
            "SWSWWSWSWWSWW",
            "SWSWWSW",
            "SWSWWSWW"
        ],
        "alcaicA": [
            "WSWSWSWWSWW",
            "WSWSWSWWSWW",
            "WSWSWSWSW",
            "SWWSWWSWSW",
        ],
        "alcaicB": [
            "SWSWWSWWSWW",
            "SWSWWSWWSWW",
            "SWSWSWSWW",
            "SWWSWWSWSW",
        ],
    }

    # Hexametre regex
    HEXAMETRE_REGEX = re.compile(r"^SWW?SWW?SWW?SWW?SWW?SW$")

    # Pentametre regex
    PENTAMETRE_REGEX = re.compile(r"^SWW?SWW?SW?SWW?SWW?S$")

    # Hexametre syllable count
    HEXAMETRE_SYLLABLE_CNT = range(12, 18)

    # Pentametre syllable count
    PENTAMETRE_SYLLABLE_CNT = range(10, 16)

    # Max syllable count in one line that is processed
    MAX_LINE_SYLLABLE_CNT = 26

    def _generate_all_valid_line_patterns(self, syllable_cnt: int, regex: re.Pattern) -> Iterable:
        """
        Generate all valid line metrical patterns for a given syllable count.
        :param syllable_cnt: Syllable count
        :param regex: Regex to test whether a pattern is valid
        :return: Valid line metrical patterns
        """
        if syllable_cnt > self.MAX_LINE_SYLLABLE_CNT:
            return []

        all_combs = ["".join(pos) for pos in product(self.METRICAL_POSITIONS, repeat=syllable_cnt)]
        return filter(regex.match, all_combs)

    def _generate_all_valid_syllabotonic_line_patterns(self, syllable_cnt: int) -> Iterable:
        """
        Generate all valid syllabotonic line metrical patterns for a given syllable count.
        :param syllable_cnt: Syllable count
        :return: Valid syllabotonic line metrical patterns
        """
        return self._generate_all_valid_line_patterns(syllable_cnt, self.SYLLABOTONIC_REGEX)

    def _generate_all_valid_hexametre_line_patterns(self, syllable_cnt: int) -> Iterable:
        """
        Generate all valid hexametre line metrical patterns for a given syllable count.
        :param syllable_cnt: Syllable count
        :return: Valid hexametre line metrical patterns
        """
        return self._generate_all_valid_line_patterns(syllable_cnt, self.HEXAMETRE_REGEX)

    def _generate_all_valid_pentametre_line_patterns(self, syllable_cnt: int) -> Iterable:
        """
        Generate all valid pentametre line metrical patterns for a given syllable count.
        :param syllable_cnt: Syllable count
        :return: Valid pentametre line metrical patterns
        """
        return self._generate_all_valid_line_patterns(syllable_cnt, self.PENTAMETRE_REGEX)

    @staticmethod
    def _get_line_syllable_cnt(line_syllable_classes: list) -> int:
        """
        Return syllable count of a line.
        :param line_syllable_classes: Syllable clases of the line
        :return: Syllable count of the line
        """
        return sum(len(token_syllables) for token_syllables in line_syllable_classes)

    def _get_max_syllable_cnt(self, poem_syllable_classes: list) -> int:
        """
        Return maximal syllable count of all poem lines.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Maximal syllable count of all poem lines
        """
        return max(self._get_line_syllable_cnt(line) for line in poem_syllable_classes)

    def _check_all_lines_syllable_cnt_in_interval(self, poem_syllable_classes: list, interval: Iterable) -> bool:
        """
        Check whether syllable counts of all poem lines are in a given interval.
        :param poem_syllable_classes: Syllable classes of the poem
        :param interval: Interval
        :return: Whether syllable counts of all poem lines are in the interval
        """
        return all(self._get_line_syllable_cnt(line) in interval for line in poem_syllable_classes)

    def _poem_can_be_hexametre(self, poem_syllable_classes: list) -> bool:
        """
        Decide whether a poem can be hexametre based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Whether the poem can be hexametre
        """
        return self._check_all_lines_syllable_cnt_in_interval(poem_syllable_classes, self.HEXAMETRE_SYLLABLE_CNT)

    def _poem_can_be_pentametre(self, poem_syllable_classes: list) -> bool:
        """
        Decide whether a poem can be pentametre based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Whether the poem can be pentametre
        """
        return self._check_all_lines_syllable_cnt_in_interval(poem_syllable_classes, self.PENTAMETRE_SYLLABLE_CNT)

    def _poem_can_be_elegiac_couplet(self, poem_syllable_classes: list) -> bool:
        """
        Decide whether a poem can be elegiac couplet based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Whether the poem can be elegiac couplet
        """
        odd_lines = poem_syllable_classes[::2]
        even_lines = poem_syllable_classes[1::2]

        return all((self._poem_can_be_hexametre([line]) for line in odd_lines)) and all((self._poem_can_be_pentametre([line]) for line in even_lines))

    def _generate_all_two_dimensional_patterns(self, poem_syllable_classes: list, generate_func: Callable) -> list:
        """
        Generate all possible two-dimensional metrical patterns for a poem based on its syllable counts and given generating function.
        :param poem_syllable_classes: Syllable classes of the poem
        :param generate_func: Generating function
        :return: Generated metrical patterns
        """
        return [[pattern for pattern in generate_func(self._get_line_syllable_cnt(line))] for line in poem_syllable_classes]

    def _generate_all_hexametre_patterns(self, poem_syllable_classes: list) -> list:
        """
        Generate all possible hexametre patterns for a poem based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Generated hexametre patterns
        """
        return self._generate_all_two_dimensional_patterns(poem_syllable_classes, self._generate_all_valid_hexametre_line_patterns)

    def _generate_all_pentametre_patterns(self, poem_syllable_classes: list) -> list:
        """
        Generate all possible pentametre patterns for a poem based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Generated pentametre patterns
        """
        return self._generate_all_two_dimensional_patterns(poem_syllable_classes, self._generate_all_valid_pentametre_line_patterns)

    def _generate_all_elegiac_couplet_patterns(self, poem_syllable_classes: list) -> list:
        """
        Generate all possible elegiac couplet patterns for a poem based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Generated elegiac couplet patterns
        """
        all_elegiac_couplets = []

        for line_idx, line in enumerate(poem_syllable_classes):
            if line_idx % 2 == 0:
                all_elegiac_couplets += self._generate_all_hexametre_patterns([line])
            else:
                all_elegiac_couplets += self._generate_all_pentametre_patterns([line])

        return all_elegiac_couplets

    def _generate_all_hexametres_pentametres_elegiac_couplets(self, poem_syllable_classes: list) -> dict:
        """
        Generate all possible hexametres, pentametres and elegiac couplets for a poem based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Generated hexametres, pentametres and elegiac couplets
        """
        all_metres = {}

        if self._poem_can_be_hexametre(poem_syllable_classes):
            all_metres.update({"hexametre": self._generate_all_hexametre_patterns(poem_syllable_classes)})
        if self._poem_can_be_pentametre(poem_syllable_classes):
            all_metres.update({"pentametre": self._generate_all_pentametre_patterns(poem_syllable_classes)})
        if self._poem_can_be_elegiac_couplet(poem_syllable_classes):
            all_metres.update({"elegiac": self._generate_all_elegiac_couplet_patterns(poem_syllable_classes)})

        return all_metres

    def _generate_all_quantitative_syllabic_strophes(self, poem_syllable_classes: list) -> dict:
        """
        Generate all possible quantitative syllabic strophes for a poem based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Generated quantitative syllabic strophes
        """
        all_metres = {}

        poem_line_cnt = len(poem_syllable_classes)

        for metre_name, strophe in self.QUANTITATIVE_SYLLABIC_STROPHES_PATTERNS.items():
            strophe_line_cnt = len(strophe)

            if poem_line_cnt % strophe_line_cnt == 0:
                strophe_idx = 0
                ok = True

                for line_idx in range(poem_line_cnt):
                    if self._get_line_syllable_cnt(poem_syllable_classes[line_idx]) != len(strophe[strophe_idx]):
                        ok = False
                        break

                    strophe_idx += 1

                    if strophe_idx == strophe_line_cnt:
                        strophe_idx = 0

                if ok:
                    strophe_cnt = poem_line_cnt // strophe_line_cnt
                    all_metres[metre_name] = strophe_cnt * strophe

        return all_metres

    def _generate_all_standard_syllabotonic_metres(self, poem_syllable_classes: list) -> dict:
        """
        Generate all possible standard syllabotonic metres for a poem based on its line syllable counts.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Generated standard syllabotonic metres
        """
        all_metres = {}

        max_syll_cnt = self._get_max_syllable_cnt(poem_syllable_classes)
        valid_patterns = self._generate_all_valid_syllabotonic_line_patterns(max_syll_cnt)

        for pattern_str in valid_patterns:
            line_patterns = [pattern_str[: self._get_line_syllable_cnt(line)] for line in poem_syllable_classes]
            all_metres[pattern_str] = line_patterns

        return all_metres

    def _generate_all_metres_non_ghazal_poem(self, poem_syllable_classes: list) -> dict:
        """
        Generate all possible metres for a non-ghazal poem.
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Generated metres
        """
        all_metres = {}

        # Standard syllabotonic metres
        all_metres.update(self._generate_all_standard_syllabotonic_metres(poem_syllable_classes))
        # Sapphic, Asclepiad, AlcaicA, AlcaicB stanzas
        all_metres.update(self._generate_all_quantitative_syllabic_strophes(poem_syllable_classes))
        # Hexametres, Pentametres, Elegiac couplets
        all_metres.update(self._generate_all_hexametres_pentametres_elegiac_couplets(poem_syllable_classes))

        return all_metres

    def _merge_ghazal_parts_patterns(self, non_radif_metrical_pattern: list, radif_metrical_pattern: list, only_radif_line_idxs: List[int]) -> list:
        """
        For a ghazal poem merge a metrical pattern generated for the non-radif part and a metrical pattern generated for the radif-part into one metrical pattern.
        :param non_radif_metrical_pattern: Metrical pattern generated for the non-radif part
        :param radif_metrical_pattern: Metrical pattern generated for the radif part
        :param only_radif_line_idxs: Idxs of lines that contain only a radif
        :return: Merged patterns
        """
        ghazal_pattern = []

        is_non_radif_pattern_2d = type(non_radif_metrical_pattern[0]) == list
        non_radif_pattern = non_radif_metrical_pattern.copy()

        for empty_line_idx in only_radif_line_idxs:
            if is_non_radif_pattern_2d:
                non_radif_pattern.insert(empty_line_idx, [""])
            else:
                non_radif_pattern.insert(empty_line_idx, "")

        radif_idx = 0

        for line_idx, non_radif_line in enumerate(non_radif_pattern):
            if self._is_radif_line_idx(line_idx):
                if is_non_radif_pattern_2d:
                    ghazal_pattern.append([possible_pattern + radif_metrical_pattern[radif_idx] for possible_pattern in non_radif_line])
                else:
                    ghazal_pattern.append(non_radif_line + radif_metrical_pattern[radif_idx])
                radif_idx += 1
            else:
                ghazal_pattern.append(non_radif_line)

        return ghazal_pattern

    def _combine_ghazal_parts_metres(self, non_radif_metres: dict, radif_metres: dict, only_radif_line_idxs: List[int]) -> dict:
        """
        For a ghazal poem return Cartesian product of metres generated for the non-radif part and for the radif-part.
        :param non_radif_metres: Metres generated for the non-radif part
        :param radif_metres: Metres generated for the radif part
        :param only_radif_line_idxs: Idxs of lines that contain only a radif
        :return: Cartesian product of metres
        """
        all_metres = {}

        for radif_metre_name, radif_metrical_pattern in radif_metres.items():
            for non_radif_metre_name, non_radif_metrical_pattern in non_radif_metres.items():
                ghazal_metre_name = f"ghazal({non_radif_metre_name}+{radif_metre_name})"
                ghazal_pattern = self._merge_ghazal_parts_patterns(non_radif_metrical_pattern, radif_metrical_pattern, only_radif_line_idxs)
                all_metres[ghazal_metre_name] = ghazal_pattern

        return all_metres

    @staticmethod
    def _is_radif_line_idx(line_idx: int) -> bool:
        """
        Test whether in this line ghazal poem must end with radif.
        :param line_idx: Line idx
        :return: Whether in this line ghazal poem must end with radif
        """
        return line_idx == 0 or line_idx % 2 == 1

    def _split_ghazal_syllable_classes(self, poem_syllable_classes: list, radif_word_cnt: int) -> Tuple[list, list, list]:
        """
        Split Syllable classes of a ghazal poem into a part without a radif and a part containing a radif.
        Return also idxs of lines that contain only radifs.
        :param poem_syllable_classes: Syllable classes of a poem
        :param radif_word_cnt: Word count of the radif
        :return: Syllable classes of a part without a radif, Syllable classes of a part with radif and line idxs of lines containing only radifs
        """
        non_radif_syll_classes = []
        radif_syll_classes = []
        only_radif_line_idxs = []

        for idx, line in enumerate(poem_syllable_classes):
            if self._is_radif_line_idx(idx):
                non_radif_part = line[:-radif_word_cnt]
                radif_part = line[-radif_word_cnt:]
                radif_syll_classes.append(radif_part)

                if len(non_radif_part) > 0:
                    non_radif_syll_classes.append(non_radif_part)
                else:
                    only_radif_line_idxs.append(idx)
            else:
                non_radif_syll_classes.append(line)

        return non_radif_syll_classes, radif_syll_classes, only_radif_line_idxs

    def _generate_all_metres_ghazal_poem(self, poem_syllable_classes: list, radif_word_cnt: int) -> dict:
        """
        Generate all possible metres for a ghazal poem.
        :param poem_syllable_classes: Syllable classes of the poem
        :param radif_word_cnt: Word count of the radif
        :return: Generated metres
        """
        non_radif_syll_classes, radif_syll_classes, empty_non_radif_line_idxs = self._split_ghazal_syllable_classes(poem_syllable_classes, radif_word_cnt)
        non_radif_metres = self._generate_all_metres_non_ghazal_poem(non_radif_syll_classes)
        radif_metres = self._generate_all_standard_syllabotonic_metres(radif_syll_classes)

        return self._combine_ghazal_parts_metres(non_radif_metres, radif_metres, empty_non_radif_line_idxs)

    @staticmethod
    def _get_radif(poem_tokens: list) -> Optional[List[str]]:
        """
        Extract radif from a poem.
        :param poem_tokens: Tokens of the poem
        :return: Extracted radif, None for a non-ghazal poem
        """
        radif = None

        if len(poem_tokens) < 2:
            return None

        even_lines = poem_tokens[1::2]
        ghazal_lines = [poem_tokens[0]] + even_lines
        max_radif_len = min(len(line) for line in ghazal_lines)

        for i in range(max_radif_len, 0, -1):
            subseq = poem_tokens[0][-i:]

            if all(line[-i:] == subseq for line in even_lines):
                radif = subseq
                break

        return radif

    @staticmethod
    def _get_line_tokens(line_data: List[dict]) -> List[str]:
        """
        Get line tokens.
        :param line_data: Data of the line
        :return: Line tokens
        """
        return [word["token_lc"] for word in line_data]

    def _get_poem_tokens(self, poem_data: list) -> list:
        """
        Get poem tokens.
        :param poem_data: Data of the poem
        :return: Poem tokens
        """
        return [self._get_line_tokens(line_data) for line_data in poem_data]

    def generate_all_metres_poem(self, poem_syllable_classes: list, poem_data: list) -> dict:
        """
        Generate all possible metres for a poem.
        :param poem_syllable_classes: Syllable classes of the poem
        :param poem_data: Poem data
        :return: Generated metres
        """
        poem_tokens = self._get_poem_tokens(poem_data)
        radif = self._get_radif(poem_tokens)

        if radif:
            return self._generate_all_metres_ghazal_poem(poem_syllable_classes, len(radif))
        else:
            return self._generate_all_metres_non_ghazal_poem(poem_syllable_classes)

    def generate_all_metres_poems(self, poems_syllable_classes: list, poems_data: list) -> list:
        """
        Generate all possible metres for poems.
        :param poems_syllable_classes: Syllable classes of the poems
        :param poems_data: Poems data
        :return: Generated metres
        """
        return [self.generate_all_metres_poem(poem_syllable_classes, poem_data) for poem_syllable_classes, poem_data in zip(poems_syllable_classes, poems_data)]
