def find_sense(sense_name, senseMap):
    for k, v in senseMap.items():
        if sense_name in v:
            return v[sense_name]


def statistics(dict1, dict2):
    # value = {k: dict2[k] for k in set(dict2) - set(dict1)}
    print('value:\n', set(dict2) - set(dict1))
    # return value
