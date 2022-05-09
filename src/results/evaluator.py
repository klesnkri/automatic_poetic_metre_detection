from sklearn.metrics import accuracy_score
from typing import List


class Evaluator:
    """Evaluator to evaluate accuracies of metrical tagging predictions."""

    def __init__(self, ref_predictions: list) -> None:
        """
        :param ref_predictions: Referential predictions to test against
        """
        self.ref_syll_predictions = self.get_syll_predictions(ref_predictions)
        self.ref_line_predictions = self.get_line_predictions(ref_predictions)
        self.ref_poem_predictions = self.get_poem_predictions(ref_predictions)

    @classmethod
    def get_syll_predictions(cls, predictions: list) -> List[str]:
        """
        Get syllable predictions.
        :param predictions: Input predictions
        :return: Syllable predictions
        """
        return [pos for poem in predictions for line in poem for pos in line]

    @classmethod
    def get_line_predictions(cls, predictions: list) -> List[str]:
        """
        Get line predictions.
        :param predictions: Input predictions
        :return: Line predictions
        """
        return [line for poem in predictions for line in poem]

    @classmethod
    def __get_poem_prediction_str(cls, poem_prediction: list) -> str:
        """
        Represent prediction for a poem as a string.
        :param poem_prediction: Poem prediction
        :return: String representing poem prediction
        """
        return " ".join(line for line in poem_prediction)

    @classmethod
    def get_poem_predictions(cls, predictions: list) -> List[str]:
        """
        Get poem predictions.
        :param predictions: Input predictions
        :return: Poem predictions
        """
        return [cls.__get_poem_prediction_str(poem) for poem in predictions]

    def get_syllable_accuracy(self, predictions: list) -> float:
        """
        Count syllable accuracy of predictions.
        :param predictions: Predictions to count accuracy for
        :return: Syllable accuracy
        """
        syll_predictions = self.get_syll_predictions(predictions)
        accuracy = accuracy_score(self.ref_syll_predictions, syll_predictions)
        print(f"Syllable accuracy: {accuracy * 100:.2f} % ({len(syll_predictions)} positions)")

        return accuracy

    def get_line_accuracy(self, predictions: list) -> float:
        """
        Count line accuracy of predictions.
        :param predictions: Predictions to count accuracy for
        :return: Line accuracy
        """
        line_predictions = self.get_line_predictions(predictions)
        accuracy = accuracy_score(self.ref_line_predictions, line_predictions)
        print(f"Line accuracy: {accuracy * 100:.2f} % ({len(line_predictions)} lines)")

        return accuracy

    def get_poem_accuracy(self, predictions: list) -> float:
        """
        Count poem accuracy of predictions.
        :param predictions: Predictions to count accuracy for
        :return: Poem accuracy
        """
        poem_predictions = self.get_poem_predictions(predictions)
        accuracy = accuracy_score(self.ref_poem_predictions, poem_predictions)
        print(f"Poem accuracy: {accuracy * 100:.2f} % ({len(poem_predictions)} poems)")

        return accuracy
