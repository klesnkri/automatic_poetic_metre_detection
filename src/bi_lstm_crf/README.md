# BiLSTM-CRF
## Contents
- `embeddings`: Compressed input embeddings
- `models`: Trained models
- `predictions`: Generated predictions
- `results`: Training results
- `train_bi_lstm_crf.py`: Train BiLSTM-CRF model
- `predict_bi_lstm_crf.py`: Generate predictions of trained BiLSTM-CRF model
- `syllable_input` / `token_input`
  - `data`: Dataframes saved in CSV format
  - `count_unique_input_tokens.ipynb`: Count unique model input tokens
  - `generate_word_2_vec_embeddings.ipynb`: Generate Word2Vec embeddings for model input tokens and save them into `emnlp2017-bilstm-cnn-crf/embeddings`
  - `create_dataframes.ipynb`: Create dataframes
  - `create_conll_datasets.ipynb`: Write dataframes contents into CoNLL file saved into `emnlp2017-bilstm-cnn-crf/data`
- `conll_data_saver.py`: Class to save dataframe contents into CoNLL format file
- `embeddings_saver.py`: Class to save compressed Word2Vec embeddings

## How to train BiLSTM-CRF with some input configuration
1. Generate Word2Vec embeddings and save them into `embeddings` using `generate_word_2_vec_embeddings.ipynb`
2. Create dataframe and save it into `data` using `create_dataframes.ipynb`
3. Transform the dataframe into CoNLL format and save it into `../../resources/emnlp2017-bilstm-cnn-crf/data` using `create_conll_datasets.ipynb`
5. Create Python3.6 (compatible with TensorFlow 1.8.0) virtual environment: `python3.6 -m venv venv`
6. Activate virtual environment: `source venv/bin/activate`
7. Install required packages: `pip3 install -r ../../resources/emnlp2017-bilstm-cnn-crf/requirements.txt`
9. Set configuration inside `train_bi_lstm_crf.py`
10. Train BiLSTM-CRF models: `python3 train_bi_lstm_crf.py` (trained models are saved into `models`, results are saved into `results`)
11. Set configuration inside: `predict_bi_lstm_crf.py`
12. Generate predictions of the trained model with the best development score `python3 predict_bi_lstm_crf.py` (predictions are saved into `predictions`)

### train_bi_lstm_crf.py example configuration
```
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
```

### predict_bi_lstm_crf.py example configuration
```
    DATASET_TYPE = "tokens_one_metre_all_metres_recognized_poem_line"
    MODEL_TYPE = f"line_idx_author_year_pos_lemma_15_epochs"
    MODEL_NAME = "0.9880_0.9877_13.h5"
```
