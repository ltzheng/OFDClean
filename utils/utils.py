import pandas as pd


def read_data():
    data_path = 'data.csv'
    senses_path = 'senses.csv'
    test_threshold = 0.2
    test_data = pd.read_csv(data_path)
    sense_set = pd.read_csv(senses_path, header=None, index_col=0)

    sense_set = sense_set.to_dict()[1]
    sense_set = sense2str(sense_set)
    print('senses:', sense_set)

    return test_data, sense_set

# get the num of functional dependencies
def get_attribute(data):
    return data['A'].unique(), data['B'].unique()


# convert element in senses to string format
def sense2str(senses):
    for i in senses:
        senses[i] = str(senses[i])
    return senses
