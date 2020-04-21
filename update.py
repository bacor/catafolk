import os
# import argparse
from catafolk.dataset import Dataset

if __name__ == '__main__':
    # TODO add command line args?
    datasets = [
        # # 'bronson-child-ballads',
        # # 'densmore-ojibway',
        # # 'densmore-pawnee',
        # # 'densmore-teton-sioux',
        # 'essen-china-han',
        # 'essen-china-natmin',
        # 'essen-china-shanxi',
        # 'essen-china-xinhua',
        # 'boehme-altdeutsches-liederbuch',
        # 'erk-deutscher-liederhort',
        # 'creighton-nova-scotia',
        # 'natural-history-of-song',
        # 'sagrillo-ireland',
        # 'sagrillo-luxembourg',
        # 'haydn-scottish-songs',
        'densmore-pueblo',
        # 'densmore-nootka',
        # 'finnish-folk-tunes'
        # 'boehme-volksthumliche-lieder',
        # 'pinck-verklingende-weisen'
    ]
    for dataset_id in datasets:
        print(dataset_id)
        dataset = Dataset(dataset_id)
        dataset.make()
        # dataset.plot_transformations()
    