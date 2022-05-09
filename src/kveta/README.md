# KVETA data-driven approach reimplementation
## Contents
- `data`: Saved KVETA probabilities and predictions
- `train_kveta.ipynb`: Train KVETA
- `predict_kveta.ipynb`: Generate KVETA predictions
- `sampa_syllable_parser.py`: Class to parse token to X-SAMPA syllables using its X-SAMPA transcription
- `syllable_class_parser.py`: Class to obtain Syllable class for a syllable
- `metre_generator.py`: Class to generate all possible metres for a poem based on its syllable counts
- `metre_assigner.py`: Class to assign the most probable metre to a poem
- `metre_predictor.py`: Class to predict metrical patterns for poems