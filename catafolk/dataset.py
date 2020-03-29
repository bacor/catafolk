import os
import glob
import json 
import pandas as pd
import hashlib
import re
import warnings

from file import get_file
from file import is_supported_format

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
    
    def __init__(self, data_dir, index_path, props_path,
        file_pattern, file_encoding='utf-8', file_format='infer', 
        file_preview_url=None,
        default_field_values={},
        override_field_values={},
        meta_fields_conversion={}, 
        meta_values_conversion={},
        corrections={},
        dataset_id=None,
        metadata_tables=[]):

        if not os.path.exists(data_dir):
            raise FileExistsError('The data directory does not exist')
        if not (is_supported_format(file_format) or file_format == 'infer'):
            raise ValueError(f'File format {file_format} not supported')
        
        self.data_dir = data_dir
        self.index_path = index_path
        self.props_path = props_path
        self.file_pattern = file_pattern
        self.file_encoding = file_encoding
        self.file_format = file_format
        
        self.metadata_tables = metadata_tables
        self.default_field_values = default_field_values
        self.override_field_values = override_field_values
        self.meta_fields_conversion = meta_fields_conversion
        self.meta_values_conversion = meta_values_conversion
        self.corrections = corrections
        self.dataset_id = dataset_id

        self._files = {}
        self._metadata_tables = {}
        self._index = None

    @property
    def files(self):
        if len(self._files) == 0:
            pattern = os.path.join(self.data_dir, self.file_pattern)
            for path in glob.glob(pattern):
                file = get_file(path, encoding=self.file_encoding)
                if file.id in self._files:
                    raise ValueError(f'Duplicate file id: {file.id} ({path})')
                self._files[file.id] = file

        if len(self._files) == 0:
            warnings.warn('No files were found!')

        return self._files

    def read_metadata_tables(self):
        if len(self.metadata_tables) == 0:
            return pd.DataFrame()

        dataframes = []
        for table in self.metadata_tables:
            table_name = os.path.basename(table['path'])[:-4]
            path = os.path.join(self.data_dir, table['path'])
            df = pd.read_csv(os.path.join(self.data_dir, path))
            if 'index_pattern' in table:
                pattern = table['index_pattern']
                index_col = df[table['index_col']]
                index = [pattern.format(value) for value in index_col]
                df['__id'] = index
                df.set_index('__id', inplace=True)
            elif 'index_col' in table:
                df.set_index(table['index_col'], inplace=True)
            
            df.index.name = '__song_id'
            columns = [f'{table_name}_{col}' for col in df.columns]
            df.columns = columns
            dataframes.append(df)
        
        # Merge dataframes
        metadata = dataframes[0]
        if len(dataframes) > 1:
            for df in dataframes[1:]:
                metadata = metadata.merge(df, left_on='__song_id', right_on='__song_id')

        return  metadata

    def save_index(self):
        items = []
        
        # Read out metadata tables
        metadata = self.read_metadata_tables()
        
        for id, file in self.files.items():
             # Default field values: fill with data from metatables
            if id in metadata.index:
                default_field_values = {}
                default_field_values.update(self.default_field_values)
                default_field_values.update(dict(metadata.loc[id,:]))
            else:
                default_field_values = self.default_field_values
            default_field_values['dataset_id'] = self.dataset_id
            
            item = file.export(meta_fields_conversion=self.meta_fields_conversion,
                               meta_values_conversion=self.meta_values_conversion,
                               default_field_values=default_field_values,
                               override_field_values=self.override_field_values,
                               corrections=self.corrections,
                               data_dir=self.data_dir)
                               
            items.append(item)
        self._index = pd.DataFrame(items).set_index('id').sort_index()
        self._index.to_csv(self.index_path, index=True)
    
    @property
    def index(self):
        if self._index is None:
            if os.path.exists(self.index_path):
                self._index = pd.read_csv(self.index_path, index_col='id')
            else:
                raise FileNotFoundError('Index could not be found') 
        return self._index

    def checksum(self, refresh=False):
        if refresh:
            checksums = [file.checksum for file_id, file in self.files.items()]
        else:
            checksums = self._index['checksum'].tolist()
        hash_md5 = hashlib.md5()
        hash_md5.update(''.join(checksums).encode('utf-8'))
        return hash_md5.hexdigest()

    def save_properties(self):
        props = {}
        props['dataset_id'] = self.dataset_id
        props['num_files'] = len(self.index)
        props['checksum'] = self.checksum()
        with open(self.props_path, 'w') as handle:
            json.dump(props, handle, indent=4)

    def export(self, path):
        dataset = {}
        dataset['dataset_id'] = self.dataset_id
        dataset['num_files'] = len(self.index)
        dataset['checksum'] = self.checksum()
        dataset['songs'] = self.index.to_dict()
        with open(path, 'w') as handle:
            json.dump(dataset, handle)

def list_datasets():
    return _DATASET_IDS

def is_dataset(dataset_id):
    return dataset_id in _DATASET_IDS

def load_dataset_options(dataset_id, datasets_dir, filename='config.json'):
    # cur_dir = os.path.dirname(__file__)
    # options_fn = os.path.join(cur_dir, 'options', f'{dataset_id}.json')
    options_fn = os.path.join(datasets_dir, dataset_id, filename)
    if os.path.exists(options_fn):
        with open(options_fn, 'r') as handle:
            options = json.load(handle)
            return options
    else:
        raise FileNotFoundError(f'Options file for {dataset_id} could not be found')

def get_dataset(dataset_id, datasets_dir):
    if not is_dataset(dataset_id):
        raise ValueError('Invalid dataset id')
    data_dir = os.path.join(datasets_dir, dataset_id, 'data')
    index_path = os.path.join(datasets_dir, dataset_id, 'index.csv')
    props_path = os.path.join(datasets_dir, dataset_id, 'properties.json')
    
    config_path = os.path.join(datasets_dir, dataset_id, 'config.json')
    config = json.load(open(config_path, 'r'))
    config['dataset_id'] = dataset_id
    dataset = Dataset(data_dir, index_path, props_path, **config)
    return dataset

if __name__ == '__main__':
    cur_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(cur_dir, os.path.pardir))
    datasets_dir = os.path.join(root_dir, 'datasets')

    d = get_dataset('essen-deutschl-erk', datasets_dir)
    d.save_index()
    d.save_properties()

    # d2 = get_dataset('natural-history-of-song', data_dir, index_dir)
    # d2.save_index()
    # d2.save_properties()
