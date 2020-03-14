import os
# import argparse
from dataset import get_dataset
from dataset import list_datasets

if __name__ == '__main__':
    # TODO add command line args?
    # parser = argparse.ArgumentParser(description='Index all datasets.')
    # parser.add_argument('index_dir', type='str')
    # parser.add_argument('data_dir', type='str')

    cur_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(cur_dir, os.path.pardir))
    index_dir = os.path.join(root_dir, 'website', '_data')
    data_dir = os.path.join(root_dir, 'datasets')

    for dataset_id in list_datasets():
        d = get_dataset(dataset_id, data_dir, index_dir)
        d.save_index()
        d.save_properties()
        
    