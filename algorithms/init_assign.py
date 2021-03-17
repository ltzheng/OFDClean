from collections import Counter
from scipy import stats
import math
from statistics import median
import numpy as np


def cover(sense, attr):
    '''
    senses: a sense, i.e., a list of synonyms
    attr: a list of attribute of x
    '''
    coverage = 0
    for item in attr:
        if item in sense:
            coverage += 1

    return coverage


# Algorithm 1: Initial Assignment
def init_assign(x, ssets, sense_dict):
    '''
    x: dataframe
    senses: sense dict
    '''
    right_attr = x.iloc[:, 1].tolist()
    print('right attribute:', right_attr)
    freq = dict(Counter(right_attr))

    # k = stats.median_absolute_deviation(list(freq.values()))
    # print('k:', k)
    # MAD = dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

    median_freq = median(freq.values())
    deviation = {k: abs(v - median_freq) for k, v in freq.items()}
    deviation = dict(sorted(deviation.items(), key=lambda item: item[1], reverse=False))
    print('deviation:', deviation)

    k = len(deviation)
    print('k=', k)

    sorted_senses = []
    sorted_synonyms = list(deviation.keys())
    for syn in sorted_synonyms:
        sorted_senses.append(ssets[syn])
    print('sorted_synonyms', sorted_synonyms)
    print('sorted_senses', sorted_senses)

    # iteratively search for a sense that covers k values
    potential_set = set()
    while not potential_set:
        topk = sorted_senses[:k]
        print('topk:\n', topk)
        Lambda = set(topk[0]).intersection(*topk)
        if Lambda:
            potential_set = potential_set.union(Lambda)
        k -= 1
        if k == 0:
            break

    # select the sense with maximal tuple coverage
    potential_set = list(potential_set)
    selected_sense = potential_set[0]
    max_cover = cover(sense_dict[selected_sense], right_attr)
    for s in potential_set[1:]:
        curr_cover = cover(sense_dict[s], right_attr)
        if curr_cover > max_cover:
            selected_sense = s

    return selected_sense