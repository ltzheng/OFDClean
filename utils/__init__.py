# find synonyms given sense name
def find_sense(sense_name, senseMap):
    for k, v in senseMap.items():
        if sense_name in v:
            return v[sense_name]


# precision of 2 sense assignments for experiments
def statistics(dict1, dict2):
    precision_dict = [k for k in dict1.keys() if dict1[k] == dict2[k]]
    precision = len(precision_dict) / len(dict2)
    print('precision:', precision)
