import pandas as pd
import csv

class DataLoader(object):
    def __init__(self, config):
        """
        config(dictionary): label->path
        """
        self.data_path = config['data']
        self.ofd_path = config['ofds']
        self.sense_path = config['senses']

    def read_data(self):
        data = pd.read_csv(self.data_path)
        return data

    def read_ofds(self):
        ofds = pd.read_csv(self.ofd_path, sep='->', header=None)
        ofds.columns = ['left', 'right']

        right_attrs = []
        for index, row in ofds.iterrows():
            right_attrs.append(row['right'])
            
        return ofds, right_attrs

    def read_senses(self, right_attrs):
        """
        return format:
        {'right_attributes':
            {'sense_name1': [[synonyms1], [synonyms2], ...],
             'sense_name2': [[synonyms1], [synonyms2], ...], ...}
        }
        """
        senses = dict.fromkeys(right_attrs)  # senses for all attributes
        ssets = dict.fromkeys(right_attrs)  # map synonyms->senses

        for a in right_attrs:
            sense_table = pd.read_csv(self.sense_path + a + '.csv', sep=':', header=None)
            sense_table.columns = ['name', 'synonyms']
            sense = {k: [] for k in sense_table['name'].unique().tolist()}  # sense for an attribute
            sset = {}

            for index, row in sense_table.iterrows():
                # create sense map
                synonyms = row['synonyms'].split(',')
                sense[row['name']].append(synonyms)

                # create sset map
                for syn in synonyms:
                    if syn not in sset:
                        sset[syn] = [row['name']]
                    else:
                        if row['name'] not in sset[syn]:
                            sset[syn] += [row['name']]

            senses[a] = sense
            ssets[a] = sset

        return senses, ssets
