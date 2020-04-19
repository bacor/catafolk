import os
# import argparse
from catafolk.dataset import Dataset

if __name__ == '__main__':
    # TODO add command line args?
    datasets = [
        # 'bronson-child-ballads',
        'creighton-nova-scotia',
        # 'densmore-ojibway',
        # 'densmore-pawnee',
        # 'densmore-teton-sioux',
        # 'essen-china-han',
        # 'essen-china-natmin',
        # 'essen-china-shanxi',
        # 'essen-china-xinhua',
        # 'essen-deutschl-altdeu1',
        # 'essen-deutschl-boehme',
        # 'essen-deutschl-erk',
        # 'natural-history-of-song',
        # 'sagrillo-ireland',
        # 'sagrillo-lorraine',
        # 'sagrillo-luxembourg',
        # 'sagrillo-scotland',
        
        # 'densmore-pueblo',
        # 'densmore-nootka',
        # 'finnish-folk-tunes'
    ]
    for dataset_id in datasets:
        print(dataset_id)
        dataset = Dataset(dataset_id)
        dataset.make()
        # dataset.plot_transformations()
    