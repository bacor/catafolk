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
from .file import is_supported_format
from .file import _FIELDS
from .geocoding import Locator
from .index import Index
from .index import Source
from .index import CSVSource
from .transformer import Transformer

CUR_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(join(CUR_DIR, os.path.pardir))
DATASETS_DIR = join(ROOT_DIR, 'datasets')


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
        # The directory with the actual files; defaults to the subdir 'data'
        'data_dir': join('{dataset_dir}', 'data'),
        # Json file with all configuration params
        'config_fn': 'config.json',
        # The CSV file where all metadata is indexed
        'index_fn': 'index.csv',
        # A list of all accepted fields
        'index_fields': _FIELDS,
        # Options passed to file instances
        'file_options': {
            'encoding': 'utf-8'
        }
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
        self.options.update(self.load_config())
        self.options.update(options)
        self.validate_options()

        # Set up other files and directories
        self.data_dir = self.options['data_dir'].format(dataset_dir=self.dir)
        if not exists(self.data_dir):
            raise Exception(f'No data directory found: {self.data_dir}')

        # Set up transformer
        self.transformer = None
        if 'transformations' in self.options:
            self.transformer = Transformer(self.options['transformations'])

        # Dynamic properties
        self._files = {}
        self._metadata_tables = {}
        self._ids = None

        # Set up indexer
        self.setup_index()

    @property
    def files(self):
        if len(self._files) == 0:
            pattern = join(self.data_dir, self.options['file_pattern'])
            for path in glob.glob(pattern):
                file = get_file(path, **self.options['file_options'])
                if file.id in self._files:
                    raise ValueError(f'Duplicate file id: {file.id} ({path})')
                self._files[file.id] = file
        if len(self._files) == 0:
            warnings.warn('No files were found!')
        return self._files

    @property 
    def ids(self):
        if self._ids is None:
            self._ids = sorted(list(self.files.keys()))
        return self._ids
    
    def load_config(self):
        if not exists(self.config_path):
            logging.warn(f'No configuration file found: {self.config_path}.')
            return {}
        else:
            config = json.load(open(self.config_path, 'r'))
            logging.info(f'Configuration file loaded: {self.config_path}')
            return config

    def validate_options(self):
        if 'file_pattern' not in self.options:
            raise ValueError('No `file_pattern` option was specified')

    def setup_index(self):
        self.index_path = join(self.dir, self.options['index_fn'])
        self.index = Index(self.index_path, 
                           transformer=self.transformer,
                           fields=self.options['index_fields'])
        
        default_source = Source('', entries=self._default_source_entries())
        self.index.register_sources(default_source)

        file_source = Source('file', entries=self._metadata_source_entries())
        self.index.register_sources(file_source)
        
        #TODO register others from config file?
    
    def _default_source_entries(self):
        for entry_id, file in self.files.items():
            item = {
                'id': entry_id,
                'dataset_id': self.dataset_id,
                'format': file.format,
                'path': file.relpath(root=self.data_dir),
                'checksum': file.checksum,
            }
            yield item

    def _metadata_source_entries(self):
        for entry_id, file in self.files.items():
            item = dict(id=entry_id)
            item.update(file.metadata)
            yield item

    def make(self, clear=True):
        if clear:
            self.index.clear()
        self.index.make()

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
