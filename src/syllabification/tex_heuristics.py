from typing import List


def tex_heuristics(tex_hyphens: List[str]) -> List[str]:
    """
    Heuristics to merge one-word hyphens when performing hyphenation using Czech TeX hyphenation patterns.
    :param tex_hyphens: Hyphens of a word obtained using Czech TeX hyphenation patterns
    :return: Merged hyphens
    """
    merged_hyphens = []

    for idx, hyphen in enumerate(tex_hyphens):
        if len(merged_hyphens) > 0 and (len(hyphen) == 1 or len(merged_hyphens[-1]) == 1):
            merged_hyphens[-1] += hyphen
        else:
            merged_hyphens.append(hyphen)

    return merged_hyphens
