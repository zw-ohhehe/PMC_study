import os
import json
from numpy import random
from corpus_statistics import parse_paper
from pre_processing import tokenize, remove_stop_words, stemming

NUM_FILES = 1000


def read_to_texts(files):
    texts = []
    for file in files:
        with open(file, encoding='utf8') as f:
            data = f.read()
        parsed_result = parse_paper(data)
        text = ''
        for section, content in parsed_result['structure'].items():
            text += content
        text = stemming(remove_stop_words(tokenize(text)))
        texts.append(text)
    return texts


def read_unstructure_texts(files):
    texts = []
    for file in files:
        with open(file, encoding='utf8') as f:
            data = f.read()
        data = stemming(remove_stop_words(tokenize(data)))
        texts.append(data)
    return texts


def load_files(path):
    with open(os.path.join(path, 'results', 'file_name_complete.json')) as f:
        file_name_complete = json.load(f)
    with open(os.path.join(path, 'results', 'file_name_non_complete.json')) as f:
        file_name_non_complete = json.load(f)
    with open(os.path.join(path, 'results', 'file_name_unstructure.json')) as f:
        file_name_unstructure = json.load(f)

    file_complete = random.choice(file_name_complete, NUM_FILES)
    file__non_complete = random.choice(file_name_non_complete, NUM_FILES)
    file_unstructure = random.choice(file_name_unstructure, NUM_FILES)

    texts_complete = read_to_texts(file_complete)
    texts_non_complete = read_to_texts(file__non_complete)
    texts_unstructure = read_unstructure_texts(file_unstructure)

