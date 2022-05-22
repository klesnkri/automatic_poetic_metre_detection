# Evaluation of results
## Contents
- `data`: Saved referential predictions
- `evaluator.py`: Class to evaluate prediction accuracies
- `create_ref_predictions.ipynb`: Create referential predictions
- `evaluate_KVETA.ipynb`: Evaluate KVETA data-driven approach
- `evaluate_sampa_syllables_bi_lstm_crf.ipynb`: Evaluate BiLSTM-CRF models with X-SAMPA syllable input
- `evaluate_sampa_syllables_poem_line_bi_lstm_crf.ipynb`: Evaluate BiLSTM-CRF models with X-SAMPA syllable input and input sequences representing whole poems
- `evaluate_tokens_bi_lstm_crf.ipynb`: Evaluate BiLSTM-CRF models with token input
- `evaluate_tokens_poem_line_bi_lstm_crf.ipynb`: Evaluate BiLSTM-CRF models with token input and input sequences representing whole poems

## Obtained results
### All poems just 1 metre, no unknown metres

|                                                                                                                                                 | syll acc | line acc | poem acc |
|-------------------------------------------------------------------------------------------------------------------------------------------------|:--------:|:--------:|:--------:|
| KVETA                                                                                                                                           |  97.02   |  81.88   |  69.83   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables; Max epochs: 15)                                                          |  97.91   |  95.55   |  63.84   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years; Max epochs: 15)                                          |  98.14   |  95.96   |  67.00   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags; Max epochs: 15)                                |  98.69   |  96.87   |  72.28   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15)                        |  98.79   |  97.07   |  74.53   |
| BiLSTM-CRF with X-SAMPA syllable embeddings poem as line (Input: Line idx, X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15) |  99.73   |  99.18   |  92.41   |
| BiLSTM-CRF with tokens embeddings (Input: tokens; Max epochs: 15)                                                                               |    -     |  74.38   |   8.69   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years; Max epochs: 15)                                                               |    -     |  75.91   |  10.29   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags; Max epochs: 15)                                                     |    -     |  76.94   |  11.17   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags, lemmas; Max epochs: 15)                                             |    -     |  90.01   |  31.83   |
| BiLSTM-CRF with tokens embeddings poem as line (Input: Line idx, tokens, authors, years, POS tags, lemmas; Max epochs: 15)                      |    -     |  95.47   |  55.74   |

### All lines just 1 metre, no unknown metres

|                                                                                                                                                            | syll acc | line acc | poem acc |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------:|:--------:|:--------:|
| KVETA                                                                                                                                                      |  96.08   |  80.64   |  68.26   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables; Max epochs: 15)                                                                     |  97.82   |  95.29   |  61.79   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years; Max epochs: 15)                                                     |  98.22   |  96.05   |  65.33   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags; Max epochs: 15)                                           |  98.76   |  96.98   |  72.21   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15)                                   |  98.85   |  97.17   |  74.20   |
| BiLSTM-CRF with X-SAMPA syllable embeddings poem as line (Input: Line idx, X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15)            |  99.60   |  98.81   |  90.75   |
| BiLSTM-CRF with tokens embeddings (Input: tokens; Max epochs: 15)                                                                                          |    -     |  72.14   |   7.56   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years; Max epochs: 15)                                                                          |    -     |  76.60   |   9.64   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags; Max epochs: 15)                                                                |    -     |  78.40   |  11.27   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags, lemmas; Max epochs: 15)                                                        |    -     |  91.42   |  35.39   |
| BiLSTM-CRF with tokens embeddings poem as line (Input: Line idx, tokens, authors, years, POS tags, lemmas; Max epochs: 15)                                 |    -     |  95.91   |  58.98   |