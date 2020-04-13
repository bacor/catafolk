import os
from os.path import join
from os.path import exists
import glob
import json 
import pandas as pd
import hashlib
import re
import warnings
import logging

from .file import get_file
from .geocoding import Locator
from .index import Index
from .source import *
from .transformer import Transformer

CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(join(CUR_DIR, os.path.pardir))
DATASETS_DIR = join(ROOT_DIR, 'datasets')

_FIELDS = ['dataset_id', 
           'id', 'title', 'title_eng', 'location', 'latitude', 'longitude', 
           'culture', 
           'collection_date', 'collector', 'performer',
           'source', 'source_key', 'source_author', 'source_title', 'source_publisher', 'source_address',
           'source_page_num', 'source_song_num', 'source_date', 'catalogue_number', 'source_url',
           'encoder',
           'encoding_date', 'copyright', 'license_abbr', 'version', 'meter',
           'metric_classification',
           'modality', 'key', 'ambitus', 'has_lyrics', 'has_music', 
           'genre', 'language', 'language_iso', 
           'url', 'preview_url', 'path', 'format', 'checksum']

# List of all included datasets
_DATASET_IDS = [
    'densmore-teton-sioux',
    'densmore-pawnee',
    'densmore-ojibway',
    'sagrillo-ireland',
    'sagrillo-scotland',
    'sagrillo-lorraine',
    'sagrillo-luxembourg',
    'essen-china-han',
    'essen-china-natmin',
    'essen-china-shanxi',
    'essen-china-xinhua',
    'essen-deutschl-boehme',
    'essen-deutschl-erk',
    'essen-deutschl-altdeu1',
    'creighton-nova-scotia',
    'bronson-child-ballads',
    'natural-history-of-song'
]

class Dataset(object):

    _default_options = {
        # The root dataset directory
        'dir': join(DATASETS_DIR, '{dataset_id}'),
        # Json file with all configuration params
        'config_fn': 'config.json',
        # The CSV file where all metadata is indexed
        'index_fn': 'index.csv',
        # A list of all accepted fields
        'index_fields': _FIELDS
    }

    def __init__(self, dataset_id, options={}):
        self.dataset_id = dataset_id
        
        # Set up options required to load the config file
        self.options = {}
        self.options.update(self._default_options)
        self.options.update(options)

        # Set up directories required to load the config file
        self.dir = self.options['dir'].format(dataset_id=dataset_id)
        if not exists(self.dir):
            raise Exception(f'Dataset directory does not exist: {self.dir}')
        self.config_path = join(self.dir, self.options['config_fn'])
        
        # Now load the remaining options from the config file and validate
        self.options.update(self._load_config())
        self.options.update(options)

        # Set up transformer
        self.transformer = None
        if 'transformations' in self.options:
            self.transformer = Transformer(self.options['transformations'])

        self._setup_index()

    def _load_config(self):
        if not exists(self.config_path):
            logging.warn(f'No configuration file found: {self.config_path}.')
            return {}
        else:
            config = json.load(open(self.config_path, 'r'))
            logging.info(f'Configuration file loaded: {self.config_path}')
            return config

    def _setup_index(self):
        self.index_path = join(self.dir, self.options['index_fn'])
        self.index = Index(self.index_path, 
                           transformer=self.transformer,
                           fields=self.options['index_fields'])

        if "sources" in self.options:
            for name, options in self.options['sources'].items():
                kwargs = dict(name=name)
                
                if 'id_transformations' in options:
                    transformer = Transformer(options['id_transformations'])
                    kwargs['id_transformer'] = transformer                    

                if options['type'] == 'file':
                    kwargs['data_dir'] = self.dir
                    kwargs['file_pattern'] = options.get('file_pattern')
                    if 'file_options' in options:
                        kwargs['file_options'] = options['file_options']
                    source = FileSource(**kwargs)
                    self.index.register_sources(source)

                elif options['type'] == 'csv':
                    kwargs['id_field'] = options.get('id_field')
                    path = join(self.dir, options['path'])
                    source = CSVSource(path, **kwargs)
                    self.index.register_sources(source)

    def make(self, clear=True):
        if clear:
            self.index.clear()
        self.index.make()

    def plot_transformations(self):
        path = join(self.dir, 'transformations.pdf')
        self.transformer.plot(path)

    def checksum(self, refresh=False):
        if refresh:
            checksums = [file.checksum for file_id, file in self.files.items()]
        else:
            checksums = self._index['checksum'].tolist()
        hash_md5 = hashlib.md5()
        hash_md5.update(''.join(checksums).encode('utf-8'))
        return hash_md5.hexdigest()

def list_datasets():
    return _DATASET_IDS

def is_dataset(dataset_id):
    return dataset_id in _DATASET_IDS
