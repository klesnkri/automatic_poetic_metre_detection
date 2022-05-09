import json
from typing import List
import logging
import sys
import os

# Get absolute paths of dirs
this_dir = os.path.abspath(".")
to_go_dir = os.path.abspath("../../resources/emnlp2017-bilstm-cnn-crf")

# Add to path
sys.path.append(to_go_dir)

# Change dir
os.chdir(to_go_dir)

from util.preprocessing import readCoNLL, createMatrices
from neuralnets.BiLSTM import BiLSTM

# Logging level
loggingLevel = logging.INFO
logger = logging.getLogger()
logger.setLevel(loggingLevel)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(loggingLevel)
formatter = logging.Formatter("%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

EMPTY_POS = "_"


def split_predictions_by_line(predictions: list, test_matrix: List[dict]) -> list:
    """
    Normalize poem-level predictions splitting them by line.
    :param predictions: Obtained predictions
    :param test_matrix: Test matrix
    :return: Split predictions
    """
    logger.info("Splitting predictions by line...")
    predictions_split_by_line = []

    for poem_predictions, poem_test_matrix in zip(predictions, test_matrix):
        poem_predictions_split_by_line = []
        last_line_idx = None

        for line_idx, metre_pos in zip(poem_test_matrix["lineIdx"], poem_predictions):
            metre_pos = metre_pos.replace(EMPTY_POS, "")

            if line_idx != last_line_idx:
                poem_predictions_split_by_line.append(metre_pos)
            else:
                poem_predictions_split_by_line[-1] += metre_pos

            last_line_idx = line_idx

        predictions_split_by_line.append(poem_predictions_split_by_line)

    logger.info("Predictions split by line.")

    return predictions_split_by_line


def split_predictions_by_poem(predictions: list, test_matrix: List[dict]) -> list:
    """
    Normalize line-level predictions splitting them by poem.
    :param predictions: Obtained predictions
    :param test_matrix: Test matrix
    :return: Split predictions
    """
    logger.info("Splitting predictions by poem...")
    predictions_split_by_poem = []
    last_poem_idx = None

    for line_predictions, line_test_matrix in zip(predictions, test_matrix):
        poem_idx = line_test_matrix["poemIdx"][0]
        line_str = "".join(pos.replace(EMPTY_POS, "") for pos in line_predictions)

        if poem_idx != last_poem_idx:
            predictions_split_by_poem.append([line_str])
        else:
            predictions_split_by_poem[-1].append(line_str)

        last_poem_idx = poem_idx

    logger.info("Predictions split by poem.")

    return predictions_split_by_poem


def predict(dataset_type: str, model_type: str, model_name: str) -> None:
    """
    Generate Corpus of Czech Verse predictions in standard format obtained from trained BiLSTM-CRF model and save them into file.
    :param dataset_type: Type of dataset
    :param model_type: Type of model
    :param model_name: Name of the trained model to use
    """
    dataset_name = f"ccv_{dataset_type}"
    model_path = os.path.join(this_dir, f"models/{dataset_type}/{model_type}/{model_name}")

    if dataset_type.startswith("tokens"):
        input_columns = {0: "poemIdx", 1: "lineIdx", 3: "tokens", 4: "author", 5: "year", 6: "pos", 7: "lemma", 8: "metrePos"}
    else:
        input_columns = {0: "poemIdx", 1: "lineIdx", 4: "syllableCls", 5: "tokens", 6: "author", 7: "year", 8: "pos", 9: "metrePos", 10: "lemma"}

    test_sentences = readCoNLL(f"data/{dataset_name}/test.txt", input_columns)
    trained_model = BiLSTM.loadModel(model_path)
    test_matrix = createMatrices(test_sentences, trained_model.mappings, True)
    predictions = trained_model.tagSentences(test_matrix)[dataset_name]

    if "_poem_line" in dataset_type:
        predictions = split_predictions_by_line(predictions, test_matrix)
    else:
        predictions = split_predictions_by_poem(predictions, test_matrix)

    predictions_file_path = os.path.join(this_dir, f"predictions/{dataset_type}/{model_type}.json")

    with open(predictions_file_path, "w") as f:
        json.dump(predictions, f)

    logger.info(f"Predictions saved.")


if __name__ == "__main__":
    DATASET_TYPE = "tokens_one_metre_all_metres_recognized_poem_line"
    MODEL_TYPE = f"line_idx_author_year_pos_lemma_15_epochs"
    MODEL_NAME = "0.9880_0.9877_13.h5"

    predict(DATASET_TYPE, MODEL_TYPE, MODEL_NAME)
