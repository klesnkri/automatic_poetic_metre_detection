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
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables; Max epochs: 15)                                                          |  97.93   |  95.67   |  66.78   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years; Max epochs: 15)                                          |  98.14   |  95.97   |  66.29   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags; Max epochs: 15)                                |  98.69   |  96.85   |  72.34   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15)                        |  98.74   |  96.94   |  72.98   |
| BiLSTM-CRF with X-SAMPA syllable embeddings poem as line (Input: Line idx, X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15) |  99.71   |  99.17   |  92.51   |
| BiLSTM-CRF with tokens embeddings (Input: tokens; Max epochs: 15)                                                                               |    -     |  74.38   |   8.69   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years; Max epochs: 15)                                                               |    -     |  75.91   |  10.29   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags; Max epochs: 15)                                                     |    -     |  76.94   |  11.17   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags, lemmas; Max epochs: 15)                                             |    -     |  90.01   |  31.83   |
| BiLSTM-CRF with tokens embeddings poem as line (Input: Line idx, tokens, authors, years, POS tags, lemmas; Max epochs: 15)                      |    -     |  95.47   |  55.74   |

### All lines just 1 metre, no unknown metres

|                                                                                                                                                            | syll acc | line acc | poem acc |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------:|:--------:|:--------:|
| KVETA                                                                                                                                                      |  96.08   |  80.64   |  68.26   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables; Max epochs: 15)                                                                     |  97.78   |  95.31   |  62.91   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years; Max epochs: 15)                                                     |  98.21   |  96.09   |  67.20   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags; Max epochs: 15)                                           |  98.72   |  96.96   |  73.41   |
| BiLSTM-CRF with X-SAMPA syllable embeddings (Input: X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15)                                   |  98.83   |  97.12   |  73.06   |
| BiLSTM-CRF with X-SAMPA syllable embeddings poem as line (Input: Line idx, X-SAMPA syllables, authors, years, POS tags, lemmas; Max epochs: 15)            |  99.61   |  98.86   |  90.40   |
| BiLSTM-CRF with tokens embeddings (Input: tokens; Max epochs: 15)                                                                                          |    -     |  72.14   |   7.56   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years; Max epochs: 15)                                                                          |    -     |  76.60   |   9.64   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags; Max epochs: 15)                                                                |    -     |  78.40   |  11.27   |
| BiLSTM-CRF with tokens embeddings (Input: tokens, authors, years, POS tags, lemmas; Max epochs: 15)                                                        |    -     |  91.42   |  35.39   |
| BiLSTM-CRF with tokens embeddings poem as line (Input: Line idx, tokens, authors, years, POS tags, lemmas; Max epochs: 15)                                 |    -     |  95.91   |  58.98   |