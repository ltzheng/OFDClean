import argparse
from utils.data_loader import DataLoader
from algorithms.OFDClean import OFDClean


if __name__ == '__main__':
    threshold = 10
    config = {
        'data': 'datasets/data/' + 'clinical.csv',
        'ofds': 'datasets/ofds/' + 'clinical.csv',
        'senses': 'datasets/senses/' + 'clinical/',  # sense name should be the same as column name
    }
    Loader = DataLoader(config)
    data = Loader.read_data()
    # print('data:\n', data)
    ofds, right_attrs = Loader.read_ofds()
    # print('ofds:\n', ofds)
    # print('right_attrs:\n', right_attrs)
    senses, ssets = Loader.read_senses(right_attrs)
    print('senses:\n', senses)
    # print('ssets:\n', ssets)

    Cleaner = OFDClean(data, ofds, senses, right_attrs, ssets, threshold)
    Cleaner.run()