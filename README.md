# Automatic Poetic Metre Detection
This repository contains source codes and all additional files for my bachelor's thesis at [FIT CTU](https://fit.cvut.cz).

## Contents
- `text`: Thesis text files
  - `thesis.pdf`: Thesis text in PDF format
  - `src`: Thesis text source code in LaTeX
- `resources`: Resources used inside the implementation
  - `corpusCzechVerse`: Corpus of Czech Verse Git repository
  - `emnlp2017-bilstm-cnn-crf`: BiLSTM-CRF Git repository
- `src`: Implementation
- `requirements.txt`: Python packages installation file
- `.env`: Environment variables file

## Environment for running all jupyter notebooks inside the implementation part
1. Save absolute path of this directory to `WORKING_DIR` environment variable inside `.env` file (create `.env` if not exists): `echo "WORKING_DIR=/absolute/path/to/this/dir" > .env`
2. Create Python3 virtual environment: `python3 -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install required packages: `pip3 install -r requirements.txt`

### When using this code as Git repository cloned from [GitHub](https://github.com/klesnkri/automatic_poetic_metre_detection.git)
5. Initialize Git submodules located inside `resources`: `git submodule init & git submodule update`

### When using this repository as regular non-Git folder
5. Create directory `resources`: `mkdir resources`
6. Change directory to `resources`: `cd resources`
7. Clone respected Git directories:
      - `git clone git@github.com:klesnkri/emnlp2017-bilstm-cnn-crf.git`
      - `git clone git@github.com:versotym/corpusCzechVerse.git`