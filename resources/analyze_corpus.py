from matplotlib_venn import venn3
from matplotlib import pyplot as plt
import sys
import os
import json


def find_exclusive(d1, d2, d3):
    plus, minus = [],  []
    for word in d1:
        if word not in d2 and word not in d3:
            plus.append(word)
    plus = [x for x in d1 if x not in d2 and x not in d3]

    for word in d2:
        if word in d3 and word not in d1:
            minus.append(word)
    return plus, minus


def analyze(path):
    i = sys.argv[1]
    with open(os.path.join(path, 'results', 'hf_words_c{}.json').format(i)) as f:
        word_count_c = json.load(f)
    with open(os.path.join(path, 'results', 'hf_words_nc{}.json').format(i)) as f:
        word_count_nc = json.load(f)
    with open(os.path.join(path, 'results', 'hf_words_us{}.json').format(i)) as f:
        word_count_us = json.load(f)

    c_list = [x[0] for x in word_count_c]
    nc_list = [x[0] for x in word_count_nc]
    us_list = [x[0] for x in word_count_us]

    c_plus, c_minus = find_exclusive(c_list, nc_list, us_list)
    nc_plus, nc_minus = find_exclusive(nc_list, c_list, us_list)
    us_plus, us_minus = find_exclusive(us_list, c_list, nc_list)
    print(c_plus)
    print(nc_plus)
    print(us_plus)

    venn3([set(c_list), set(nc_list), set(us_list)], ('Complete', 'Non-complete', 'unstructure'))
    plt.show()


if __name__ == '__main__':
    analyze(os.getcwd())