from utils import find_sense
import math


# def sense_reassign_cost(vals, sense1, sense2, sense_dict):
#     """
#     vals: a list of attribute values of x
#     sense1, sense2: lists of synonyms
#     sense_dict: map sense id->value synonyms
#     """
#     _, R1 = outliers(vals, sense1, sense_dict)
#     _, R2 = outliers(vals, sense2, sense_dict)
#     cost = R2 - R1
#     return cost


# overlap = self.overlap_tuples(x1, x2)[self.right_col_name].values.tolist()
# reassign_cost1 = sense_reassign_cost(val1, sense1, sense2, self.sense_dict)
# reassign_cost2 = sense_reassign_cost(val2, sense2, sense1, self.sense_dict)
# if min(reassign_cost1, reassign_cost2) < repair_cost(overlap, sense1, sense2, self.sense_dict):


# outliers w.r.t a given sense and right values
def outliers(right_val, synonyms):
    return [v for v in right_val if v not in synonyms]


class Repair(object):

    def __init__(self, eqTupleMap, senseMap, beam_size=None):
        self.eqTupleMap = eqTupleMap
        self.senseMap = senseMap
        # self.ontologyCandidates = set()
        # self.nodeSenseMap = {}
        # if not beam_size:
        #     self.beam_size = len(self.ontologyCandidates) / math.e

    # identify tuples not covered by assigned senses, maintaining ontologyCandidates and nodeSenseMap
    def identify_errors(self, left_vals, assigned_sense):
        right_val = self.eqTupleMap[left_vals]

        if assigned_sense:
            synonyms = find_sense(assigned_sense, self.senseMap)
            return len(outliers(right_val, synonyms))

            # self.ontologyCandidates.update(missed_right_val)
            # for v in missed_right_val:
            #     if v in self.nodeSenseMap:
            #         if assigned_sense not in self.nodeSenseMap[v]:
            #             self.nodeSenseMap[v] += [assigned_sense]
            #     else:
            #         self.nodeSenseMap[v] = [assigned_sense]

    # beam search to get minimal repair
    def beam_search(self):
        raise NotImplementedError
    
    # def repair_cost(self, vals, sense_name1, sense_name2):
    #     rho1, R1 = outliers(vals, sense_name1)
    #     rho2, R2 = outliers(vals, sense_name2)
    #
    #     # ontology repair cost
    #     ontology_repair_cost = len(rho1) + len(rho2)  # number of unique outlier values
    #
    #     # data_repair_cost
    #     data_repair_cost = R1 + R2
    #
    #     return ontology_repair_cost, data_repair_cost
