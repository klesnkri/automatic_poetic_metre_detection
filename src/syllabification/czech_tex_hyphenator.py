"""
Hyphenation, using Frank Liang's algorithm.
Ned Batchelder's publicly available source code hyphenate.py https://nedbatchelder.com/code/modules/hyphenate.html
modified to be used with the Czech TeX hyphenation patterns https://github.com/tensojka/cshyphen/blob/master/csskhyphen.pat.
"""

import re
import regex
from typing import List


class CzechTexHyphenator:
    """Hyphenator that supports Czech TeX hyphenation patterns."""

    def __init__(self, patterns: List[str], exceptions: List[str] = None) -> None:
        """
        :param patterns: Czech TeX hyphenation patterns
        :param exceptions: Czech TeX hyphenation patterns exceptions
        """
        # Pattern tree represented by a trie data structure
        self.tree = {}

        for pattern in patterns:
            self._insert_pattern(pattern)

        self.exceptions = {}

        if exceptions:
            for ex in exceptions:
                # Convert the hyphenated pattern into a point array
                self.exceptions[ex.replace("-", "")] = [0] + [int(h == "-") for h in regex.split(r"[\p{alpha}]", ex)]

    def _insert_pattern(self, pattern: str) -> None:
        """
        Insert pattern into the pattern tree.
        :param pattern: Pattern to be inserted
        """

        # Convert pattern like 'a1bc3d4' into a string of chars 'abcd' and a list of points [0,1,0,3,4]
        chars = re.sub(r"[0-9]", "", pattern)
        points = [int(d or 0) for d in regex.split("[.\p{alpha}]", pattern)]

        # Insert the pattern into the tree
        # Each character finds a dict another level down in the tree, and leaf nodes have the list of points
        t = self.tree

        for c in chars:
            if c not in t:
                t[c] = {}

            t = t[c]

        t[None] = points

    def hyphenate_word(self, word: str) -> List[str]:
        """
        Given a word, return a list of pieces, broken at the possible hyphenation points.
        :param word: Word to be hyphenated
        :return: Hyphens
        """
        # Short words aren't hyphenated
        if len(word) <= 4:
            return [word]

        # If the word is an exception, get the stored points
        if word.lower() in self.exceptions:
            points = self.exceptions[word.lower()]
        else:
            work = "." + word.lower() + "."
            points = [0] * (len(work) + 1)

            for i in range(len(work)):
                t = self.tree

                for c in work[i:]:
                    if c in t:
                        t = t[c]

                        if None in t:
                            p = t[None]

                            for j in range(len(p)):
                                points[i + j] = max(points[i + j], p[j])
                    else:
                        break

            # No hyphens in the first two chars or the last two
            points[1] = points[2] = points[-3] = points[-2] = 0

        # Examine the points to build the pieces list
        pieces = [""]

        for c, p in zip(word, points[2:]):
            pieces[-1] += c

            if p % 2:
                pieces.append("")

        return pieces
