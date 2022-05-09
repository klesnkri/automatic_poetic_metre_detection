import numpy as np
from scipy.stats import gmean
import re
from typing import Union, List, Tuple

from src.kveta.syllable_class_parser import SyllableClass


class MetreAssigner:
    """Class to assign the most probable metre to a poem."""

    # Regex to match names of standard syllabotonic metres
    STANDARD_SYLLABOTONIC_METRE_NAME_REGEX = re.compile(r"^(S*W*)*$")

    def __init__(self, metrical_pos_given_syll_cls_proba: dict) -> None:
        """
        :param metrical_pos_given_syll_cls_proba: Conditional probability of a metrical position given a Syllable class
        """
        self.metre_pos_given_syll_cls_proba = metrical_pos_given_syll_cls_proba

    def _get_pos_metrical_coef(self, metrical_pos: str, syll_cls: SyllableClass) -> float:
        """
        Get metrical coefficient for a metrical position as the conditional probability of its value given the corresponding Syllable class.
        :param metrical_pos: Metrical position
        :param syll_cls: Syllable class
        :return: Metrical coefficient for the metrical position
        """
        return self.metre_pos_given_syll_cls_proba[str(syll_cls)][metrical_pos]

    def _get_line_pattern_metrical_coef(self, line_pattern: str, line_syllable_classes: list) -> np.float64:
        """
        Get metrical coefficient for a line pattern as a geometric mean of metrical coefficients of its metrical positions.
        :param line_pattern: Line metrical pattern
        :param line_syllable_classes: Line Syllable classes
        :return: Metrical coefficient for the line pattern
        """
        line_syllable_classes_flatten = [syll_cls for token_syllable_classes in line_syllable_classes for syll_cls in token_syllable_classes]
        assert len(line_syllable_classes_flatten) == len(line_pattern)
        pos_coefs = [self._get_pos_metrical_coef(metre_pos, syll_cls) for (metre_pos, syll_cls) in zip(line_pattern, line_syllable_classes_flatten)]

        return gmean(pos_coefs)

    def _get_line_metrical_coef_and_selected_pattern(self, line_pattern: Union[str, List[str]], line_syllable_classes: list) -> Tuple[np.float64, str]:
        """
        Get metrical coefficient for a line and select final pattern in case of multiple line patterns (hexametre/pentametre/elegiac couplet).
        :param line_pattern: Metrical pattern of the line (can be list of metrical patterns)
        :param line_syllable_classes: Syllable classes of the line
        :return: Metrical coefficient for the line and selected pattern
        """

        # Multiple line patterns (hexametres/pentametres/elegiac couplets)
        if type(line_pattern) == list:
            all_coefs = [self._get_line_pattern_metrical_coef(pattern, line_syllable_classes) for pattern in line_pattern]
            max_idx = np.argmax(all_coefs)
            return all_coefs[max_idx], line_pattern[max_idx]
        # One line pattern
        else:
            return self._get_line_pattern_metrical_coef(line_pattern, line_syllable_classes), line_pattern

    def _get_poem_metrical_coef_and_selected_pattern(self, poem_pattern: list, poem_syllable_classes: list) -> Tuple[np.float64, list]:
        """
        Get metrical coefficient for a poem and select final pattern in case of two-dimensional metrical pattern (hexametre/pentametre/elegiac couplet).
        :param poem_pattern: Metrical pattern of the poem
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Metrical coefficient for the poem and selected pattern
        """
        assert len(poem_pattern) == len(poem_syllable_classes)

        lines_coefs_and_selected_patterns = (
            self._get_line_metrical_coef_and_selected_pattern(line_pattern, line_syllable_classes)
            for (line_pattern, line_syllable_classes) in zip(poem_pattern, poem_syllable_classes)
        )
        lines_coefs, selected_pattern = map(list, zip(*lines_coefs_and_selected_patterns))

        return gmean(lines_coefs), selected_pattern

    def assign_metre_poem(self, possible_poem_metres: dict, poem_syllable_classes: list) -> Tuple[str, list]:
        """
        Assign most probable metre to a poem.
        :param possible_poem_metres: All possible metres generated for the poem based on syllable counts
        :param poem_syllable_classes: Syllable classes of the poem
        :return: Assigned metre
        """
        metres_coefs_and_selected_patterns = (
            self._get_poem_metrical_coef_and_selected_pattern(metre_pattern, poem_syllable_classes) for metre_pattern in possible_poem_metres.values()
        )
        metres_coefs, selected_patterns = map(list, zip(*metres_coefs_and_selected_patterns))

        max_coef = max(metres_coefs)
        max_idxs = [idx for idx in range(len(metres_coefs)) if metres_coefs[idx] == max_coef]
        metres_names = list(possible_poem_metres.keys())

        # When more best patterns try to select the standard syllabotonic metre
        if len(max_idxs) > 1:
            try:
                selected_idx = next(idx for idx in max_idxs if self.STANDARD_SYLLABOTONIC_METRE_NAME_REGEX.match(metres_names[idx]))
                return metres_names[selected_idx], selected_patterns[selected_idx]
            except StopIteration:
                pass

        return metres_names[max_idxs[0]], selected_patterns[max_idxs[0]]

    def assign_metre_poems(self, possible_poems_metres: List[dict], poems_syllable_classes: list) -> List[tuple]:
        """
        Assign most probable metres to poems.
        :param possible_poems_metres: All possible metres generated for the poems based on syllable counts
        :param poems_syllable_classes: Syllable classes of the poems
        :return: Assigned metres
        """
        return [
            self.assign_metre_poem(possible_poem_metres, poem_syllable_classes)
            for (possible_poem_metres, poem_syllable_classes) in zip(possible_poems_metres, poems_syllable_classes)
        ]
