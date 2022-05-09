from typing import List

from src.kveta.syllable_class_parser import SyllableClassParser
from src.kveta.metre_generator import MetreGenerator
from src.kveta.metre_assigner import MetreAssigner
from src.kveta.sampa_syllable_parser import SampaSyllableParser


class MetrePredictor:
    """Class to predict metrical patterns for poems."""

    # Error metrical position when no patterns generated
    ERR_METRICAL_POS = "+"

    def __init__(
        self,
        sampa_parser: SampaSyllableParser,
        syllable_class_parser: SyllableClassParser,
        metre_generator: MetreGenerator,
        metre_assigner: MetreAssigner,
    ):
        """
        :param sampa_parser: Parser of X-SAMPA syllables
        :param syllable_class_parser: Parser of Syllable classes
        :param metre_generator: Generator of metres based on syllable counts
        :param metre_assigner: Assigner of the most probable generated metre
        """
        self.sampa_parser = sampa_parser
        self.syllable_class_parser = syllable_class_parser
        self.metre_generator = metre_generator
        self.metre_assigner = metre_assigner

    def predict(self, poems_data: list) -> list:
        """
        Predict metrical patterns for poems.
        :param poems_data: Poems data
        :return: Predicted metrical patterns
        """
        predicted_metrical_patterns = []

        for poem_idx, poem_data in enumerate(poems_data):
            if poem_idx % 1000 == 0:
                print(f"Analyzing poem {poem_idx}...")

            poem_sonority_peaks = self.sampa_parser.parse_poem(poem_data)
            poem_syllable_classes = self.syllable_class_parser.parse_poem(poem_sonority_peaks, poem_data)
            poem_metres = self.metre_generator.generate_all_metres_poem(poem_syllable_classes, poem_data)

            # Too many syllables, no patterns generated
            if len(poem_metres) == 0:
                print(f"Poem {poem_idx}: Too many syllables, no patterns generated, assigning error pattern...")
                predicted_metrical_pattern = ["".join(len(token) * "+" for token in line) for line in poem_sonority_peaks]
            else:
                _, predicted_metrical_pattern = self.metre_assigner.assign_metre_poem(poem_metres, poem_syllable_classes)

            predicted_metrical_patterns.append(predicted_metrical_pattern)

        return predicted_metrical_patterns
