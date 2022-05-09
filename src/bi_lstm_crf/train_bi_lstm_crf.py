import logging
import os
import sys

# Get absolute paths of dirs
this_dir = os.path.abspath(".")
to_go_dir = os.path.abspath("../../resources/emnlp2017-bilstm-cnn-crf")

# Add to path
sys.path.append(to_go_dir)

# Change dir
os.chdir(to_go_dir)

from neuralnets.BiLSTM import BiLSTM
from util.preprocessing import perpareDataset, loadDatasetPickle

# Logging level
loggingLevel = logging.INFO
logger = logging.getLogger()
logger.setLevel(loggingLevel)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(loggingLevel)
formatter = logging.Formatter("%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def train(dataset_type: str, model_type: str, num_epochs: int, params: dict, embeddings_type: str) -> None:
    """
    Train BiLSTM-CRF model on Corpus of Czech Verse data.
    :param dataset_type: Type of dataset
    :param model_type: Type of model
    :param num_epochs: Number of training epochs
    :param params: Model training hyperparameters
    :param embeddings_type: Type of embeddings
    """
    # Select dataset
    if dataset_type.startswith("tokens"):
        datasets = {
            f"ccv_{dataset_type}": {  # Name of the dataset
                "columns": {0: "poemIdx", 1: "lineIdx", 3: "tokens", 4: "author", 5: "year", 6: "pos", 7: "lemma", 8: "metrePos"},
                # CoNLL format for the input data
                "label": "metrePos",  # Which column we like to predict
                "evaluate": True,  # Should we evaluate on this task? Set true always for single task setups
                "commentSymbol": None,  # Lines in the input data starting with this string will be skipped. Can be used to skip comments
            }
        }
    else:
        datasets = {
            f"ccv_{dataset_type}": {  # Name of the dataset
                "columns": {0: "poemIdx", 1: "lineIdx", 4: "syllableCls", 5: "tokens", 6: "author", 7: "year", 8: "pos", 9: "metrePos", 10: "lemma"},
                # CoNLL format for the input data
                "label": "metrePos",  # Which column we like to predict
                "evaluate": True,  # Should we evaluate on this task? Set true always for single task setups
                "commentSymbol": None,  # Lines in the input data starting with this string will be skipped. Can be used to skip comments
            }
        }

    embeddings_path = os.path.join(this_dir, f"embeddings/embeddings_{embeddings_type}.gz")
    pickle_file = perpareDataset(embeddings_path, datasets)
    embeddings, mappings, data = loadDatasetPickle(pickle_file)

    model = BiLSTM(params)
    model.setMappings(mappings, embeddings)
    model.setDataset(datasets, data)

    results_file_path = os.path.join(this_dir, f"results/{dataset_type}/{model_type}.csv")
    model.storeResults(results_file_path)  # Path to store performance scores for dev / test

    model_file_path = os.path.join(this_dir, f"models/{dataset_type}/{model_type}/[DevScore]_[TestScore]_[Epoch].h5")
    model.modelSavePath = model_file_path  # Path to store models

    model.fit(epochs=num_epochs)


if __name__ == "__main__":
    DATASET_TYPE = "tokens_one_metre_all_metres_recognized_poem_line"
    NUM_EPOCHS = 15
    MODEL_TYPE = f"line_idx_author_year_pos_lemma_{NUM_EPOCHS}_epochs"
    EMBEDDINGS_TYPE = "tokens_one_metre_all_metres_recognized"
    PARAMS = {
        "classifier": ["CRF"],
        # Tokens have to be on the first position!!!
        "featureNames": ["tokens", "lineIdx", "author", "year", "pos", "lemma"],
        "dropout": [0.25, 0.25],
        "LSTM-Size": [100, 100, 100],
    }

    train(DATASET_TYPE, MODEL_TYPE, NUM_EPOCHS, PARAMS, EMBEDDINGS_TYPE)
