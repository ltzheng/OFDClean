from collections import Counter
from scipy import stats
import math
from statistics import median
import numpy as np


class OntologyRepair(object):

    def __init__(self, data, senses):
        self.data = data
        self.senses = senses

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


    