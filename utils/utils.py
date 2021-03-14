import pandas as pd
import csv


def read_data(data_path, senses_path, sense_num=4):
    # read data
    data = pd.read_csv(data_path)
    
    # read senses
    with open(senses_path, mode='r') as f:
        reader = csv.reader(f)
        sense_dict = {rows[0]:rows[1:] for rows in reader}

    return data, sense_dict


# get the num of functional dependencies
def get_attribute(data, col_name='A'):
    return data[col_name].unique()


# convert element in senses from int to dict
def sense2dict(sense_table):
    '''
    input: sense dataframe
    output: sense dict
    '''
    sense_dict = dict.fromkeys(sense_table.iloc[:, 0].tolist())
    # for i in senses:
    #     senses[i] = [int(i) for i in list(str(senses[i]))]
    # return senses


# convert element in senses from int to list
def sense2list(senses):
    '''
    input: {1: 123, 2: 24, 3: 145, 4: 235, 5: 125}
    output: {1: [1, 2, 3], 2: [2, 4], 3: [1, 4, 5], 4: [2, 3, 5], 5: [1, 2, 5]}
    '''
    for i in senses:
        senses[i] = [int(i) for i in list(str(senses[i]))]
    return senses


# convert element in senses from int to string
def sense2str(senses):
    '''
    input: {1: 123, 2: 24, 3: 145, 4: 235, 5: 125}
    output: {1: '123', 2: '24', 3: '145', 4: '235', 5: '125'}
    '''
    for i in senses:
        senses[i] = str(senses[i])
    return senses
