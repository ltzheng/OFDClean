import argparse
from utils.data_loader import DataLoader
from algorithms.OFDClean import OFDClean


if __name__ == '__main__':
    threshold = 20

    sense_dir = ['sense2/', 'sense4/', 'sense6/', 'sense8/', 'sense10/']
    sense_path = 'clinical'  # sense_dir[1]

    err_data_path = ['data_err3', 'data_err6', 'data_err9', 'data_err12', 'data_err15']
    size_data_path = ['data_size20', 'data_size40', 'data_size60', 'data_size80', 'data_size100']
    data_path = 'clinical'
    # data_path = err_data_path[0]
    # data_path = size_data_path[4]

    config = {
        'data': 'datasets/data/' + data_path + '.csv',
        'ofds': 'datasets/ofds/' + 'clinical.csv',
        'senses': 'datasets/senses/' + sense_path + '/',  # sense name should be the same as column name
    }
    Loader = DataLoader(config)
    data = Loader.read_data()
    # print('data:\n', data)
    ofds, right_attrs = Loader.read_ofds()
    print('ofds:\n', ofds)
    # print('right_attrs:\n', right_attrs)
    senses, ssets = Loader.read_senses(right_attrs)
    print('senses:\n', senses)
    # print('ssets:\n', ssets)

    Cleaner = OFDClean(data, ofds, senses, right_attrs, ssets, threshold)
    Cleaner.run()
