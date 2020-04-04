import os
# import argparse
from catafolk.dataset import Dataset

if __name__ == '__main__':
    # TODO add command line args?
    datasets = [
        # 'bronson-child-ballads',
        # 'creighton-nova-scotia',
        # 'densmore-ojibway',
        # 'densmore-pawnee',
        # 'densmore-teton-sioux',
        # 'sagrillo-ireland',
        # 'sagrillo-lorraine',
        # 'sagrillo-scotland',
        # 'sagrillo-luxembourg',
        # 'essen-china-han',
        # 'essen-china-natmin',
        # 'essen-china-shanxi',
        # 'essen-deutschl-erk',
        # 'essen-deutschl-boehme',
        # 'essen-deutschl-altdeu1'
        'natural-history-of-song'
    ]
    for dataset_id in datasets:
        print(dataset_id)
        dataset = Dataset(dataset_id)
        dataset.make()
        # dataset.plot_transformations()
    