from corpus_statistics import arse_paper
from pre_processing import tokenize, remove_stop_words, remove_low_frequent_words, stemming
from gensim import corpora, models as gensim_models
from numpy import random
import json
import os
import collections
import operator


PATH = 'D:\PMC'
NUM_FILES = 1000
NUM_TOPICS = 25
PASSES = 100


def get_folder_names(path):
    file_names = []
    for folder in os.listdir(path):
        for file_name in os.path.join(path, folder):
            file_names.append(os.path.join(path, folder, file_name))
    return file_names


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


def word_statistics(texts):
    data = []
    for text in texts:
        data += text
    word_count = collections.Counter(data)
    word_count = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
    print(len(word_count))
    return word_count


def lda(texts):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    ldamodel = gensim_models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=PASSES)
    return ldamodel


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

    word_count_c = word_statistics(texts_complete)
    word_count_nc = word_statistics(texts_non_complete)
    word_count_us = word_statistics(texts_unstructure)

    with open(os.path.join(path, 'results', 'hf_words_c3.json'), 'w') as f:
        json.dump(word_count_c[:100], f)
    with open(os.path.join(path, 'results', 'hf_words_nc3.json'), 'w') as f:
        json.dump(word_count_nc[:100], f)
    with open(os.path.join(path, 'results', 'hf_words_us3.json'), 'w') as f:
        json.dump(word_count_us[:100], f)


if __name__ == '__main__':
    load_files(os.getcwd())

