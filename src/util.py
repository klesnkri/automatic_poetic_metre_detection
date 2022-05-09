from typing import Optional


class Util:
    """Class with functions used by multiple notebooks."""

    RADIF_SPLIT = "-"
    SPECIAL_WEAK_POS = "V"
    DEFAULT_WEAK_POS = "W"

    @classmethod
    def normalize_metrical_pattern(cls, metrical_pattern: str) -> str:
        """
        Normalize metrical pattern to contain just 1 type of weak positions and no radif splits.
        :param metrical_pattern: Metrical pattern to normalize
        :return: Normalized metrical pattern
        """
        return metrical_pattern.replace(cls.SPECIAL_WEAK_POS, cls.DEFAULT_WEAK_POS).replace(cls.RADIF_SPLIT, "")

    @classmethod
    def get_year(cls, year_record: str) -> Optional[int]:
        """
        Extract year from year record inside the Corpus of Czech Verse data.
        :param year_record: Year as saved inside the Corpus of Czech Verse
        :return: Year in correct format
        """
        year_str = "".join(c for c in year_record if c.isdigit())
        return int(year_str) if len(year_str) > 0 else None
