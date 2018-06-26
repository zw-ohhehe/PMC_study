from pre_processing import tokenize, remove_stop_words, stemming
from corpus_statistics import parse_paper
from gensim import corpora, models as gensim_models
from numpy import random
from math import log
import os
import json
import collections

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


def generate_idf(texts, file_name):
    dct = corpora.Dictionary(texts)
    idfs = {}
    for word in dct:
        count = 0
        for text in texts:
            if word in text:
                count += 1
        if count:
            idf = log(10, len(texts) / count)
        else:
            idf = 0
    idfs[word] = idf
    with open(file_name, 'w') as f:
        json.dump(idfs, f)


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
    generate_idf(texts_complete, os.path.join(path, 'results', 'idf_c.json'))
    generate_idf(texts_non_complete, os.path.join(path, 'results', 'idf_nc.json'))
    generate_idf(texts_unstructure, os.path.join(path, 'results', 'idf_us.json'))


if __name__ == '__main__':
    load_files(os.getcwd())