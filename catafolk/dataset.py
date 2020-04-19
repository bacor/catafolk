import os
from os.path import join
from os.path import exists
import glob
import json
import yaml 
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

# Load fields from the schema file
schema_path = os.path.join(ROOT_DIR, 'index-schema.csv')
if os.path.exists(schema_path):
    schema = pd.read_csv(schema_path)
    schema.sort_values('order', ascending=True, inplace=True)
    _FIELDS = schema['field'].tolist()
else:
    warnings.warn(f'Schema file does not exist: {schema_path}')
    _FIELDS = ['id', 'dataset_id']

# TODO also move dataset options to a schema. Automatically check if
# the dataset yml file is complete/valid

class Dataset(object):

    _default_options = {
        # The root dataset directory
        'dir': join(DATASETS_DIR, '{dataset_id}'),
        # File with all configuration params
        'json_config_fn': 'config.json', # deprecated
        'config_fn': 'dataset.yml',
        'config_fields': ['transformations', 'sources'],
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
        
        # Now load the remaining options from the config file and validate
        self.options.update(self._load_config())
        self.options.update(options)

        # Set up transformer
        self.transformer = None
        if 'transformations' in self.options:
            self.transformer = Transformer(self.options['transformations'])

        self._setup_index()

    def _load_config(self):
        self.config_path = join(self.dir, self.options['config_fn'])
        self.json_config_path = join(self.dir, self.options['json_config_fn'])
        config = {}

        if exists(self.json_config_path):
            logging.warn('JSON configurations are deprecated')
            config = json.load(open(self.json_config_path, 'r'))
            logging.info(f'JSON Configuration file loaded: {self.config_path}')

        elif exists(self.config_path):
            with open(self.config_path, 'r') as stream:
                raw_config = yaml.safe_load(stream)
            for key, value in raw_config.items():
                if key in self.options['config_fields']:
                    config[key] = value
            logging.info(f'YAML Configuration file loaded: {self.config_path}')

        else:
            logging.warn(f'No configuration file found: {self.config_path}.')
        
        return config

    def _setup_index(self):
        self.index_path = join(self.dir, self.options['index_fn'])
        self.index = Index(self.index_path, 
                           transformer=self.transformer,
                           fields=self.options['index_fields'])

        if "sources" in self.options:
            for options in self.options['sources']:
                kwargs = dict(name=options['name'])
                
                if 'id_transformations' in options:
                    transformer = Transformer(options['id_transformations'])
                    kwargs['id_transformer'] = transformer                    

                if options['type'] == 'file':
                    kwargs['data_dir'] = self.dir
                    kwargs['file_pattern'] = options.get('file_pattern')
                    if 'file_options' in options:
                        kwargs['file_options'] = options['file_options']
                    if 'exclude' in options:
                        kwargs['exclude'] = options['exclude']
                    source = FileSource(**kwargs)
                    self.index.register_sources(source)

                elif options['type'] == 'csv':
                    kwargs['id_field'] = options.get('id_field')
                    if 'options' in options:
                        kwargs['options'] = options['options']
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