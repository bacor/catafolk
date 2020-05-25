import os
# import argparse
from catafolk.dataset import Dataset

if __name__ == '__main__':
    # TODO add command line args?
    datasets = [
        # # 'densmore-ojibway',
        # 'densmore-pawnee',

        # 'boehme-altdeutsches-liederbuch',
        # 'boehme-volksthumliche-lieder',
        # 'bronson-child-ballads',
        # 'creighton-nova-scotia',
        # 'densmore-menominee'
        # 'densmore-nootka',
        'densmore-papago',
        # 'densmore-pueblo',
        # 'densmore-teton-sioux',
        # 'erk-deutscher-liederhort',
        # 'essen-china-han',
        # 'essen-china-natmin',
        # 'essen-china-shanxi',
        # 'essen-china-xinhua',
        # 'finnish-folk-tunes'
        # 'haydn-scottish-songs',
        # 'natural-history-of-song',
        # 'pinck-verklingende-weisen'
        # 'sagrillo-ireland',
        # 'sagrillo-luxembourg',
    ]
    for dataset_id in datasets:
        print(dataset_id)
        dataset = Dataset(dataset_id)
        dataset.make()
        # dataset.plot_transformations()
    