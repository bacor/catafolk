import os
# import argparse
from catafolk.dataset import Dataset

if __name__ == '__main__':
    # TODO add command line args?
    # parser = argparse.ArgumentParser(description='Index all datasets.')
    # parser.add_argument('index_dir', type='str')
    # parser.add_argument('data_dir', type='str')
        
    # cur_dir = os.path.dirname(__file__)
    # root_dir = os.path.abspath(os.path.join(cur_dir, os.path.pardir))
    # datasets_dir = os.path.join(root_dir, 'datasets')

    datasets = [
        'bronson-child-ballads',
        'creighton-nova-scotia',
        'densmore-ojibway',
        'densmore-pawnee',
        'densmore-teton-sioux',
        'sagrillo-ireland',
        'sagrillo-lorraine',
        'sagrillo-scotland',
        'sagrillo-luxembourg',
        'essen-china-han',
        'essen-china-natmin',
        'essen-china-shanxi',
        'essen-deutschl-erk'
        'essen-deutschl-boehme',
        'essen-deutschl-altdeu1'
    ]
    for dataset_id in datasets:
        print(dataset_id)
        dataset = Dataset(dataset_id)
        dataset.make()
        dataset.plot_transformations()
        # d = get_dataset(dataset_id, datasets_dir)
    #     d.save_index()
    #     d.save_properties()
    
    