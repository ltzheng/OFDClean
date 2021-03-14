from collections import Counter
from scipy import stats
import math
from utils.utils import get_attribute


# return f(v) in descending order
def frequency(left_attr, values):
    counter = Counter(values)
    frequencies = {}
    for key, f in left_attr, counter:
        frequencies[key] = (counter[f] / len(values))
    frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    return frequencies


def initial_assignment(data, senses):
    left_attr, right_attr = get_attribute(data)

    freq = frequency(left_attr, right_attr)
    k = stats.median_absolute_deviation(list(freq.values()))

    potential_set = set()
    while potential_set:
        Lambda = set()
        for attr in list(freq.keys)[:k]:
            Lambda = Lambda.intersection(set(int(j) for j in senses[attr].split()))
            if Lambda:
                potential_set = potential_set.union(Lambda)
        k -= 1
