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
    'sagrillo-ireland',
    'sagrillo-scotland',
    'sagrillo-lorraine',
    'sagrillo-luxembourg'
]

class Dataset(object):

    index_columns = [
        'id',
        'title',
        'region',
        'source',
        'preview',
        'url',
        'format',
        'path',
        'checksum'
    ]

    def __init__(self, data_dir, index_path, props_path,
        file_pattern, file_encoding='utf-8', file_format='infer', 
        file_preview_url=None,
        meta_fields_map={}, 
        meta_values_map={},
        corrections={},
        shared_fields={}, dataset_id=None,):

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
        self.meta_fields_map = meta_fields_map
        self.meta_values_map = meta_values_map
        self.corrections = corrections
        self.shared_fields = shared_fields
        self.dataset_id = dataset_id

        self._files = {}
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

    def save_index(self):
        items = []
        for id, file in self.files.items():
            item = { column: None for column in self.index_columns }
            
            # Metadata
            for indexKey, metaKey in self.meta_fields_map.items():
                if indexKey in self.index_columns:
                    item[indexKey] = file.metadata.get(metaKey, None)

            # Shared fields; overrides metadata
            for field, value in self.shared_fields.items():
                if field in self.index_columns:
                    path = file.relpath(root=self.data_dir)
                    item[field] = value.format(id=file.id, path=path)

            # Finally set automatically computed fields
            item["id"] = file.id
            item["format"] = file.format
            item["path"] = file.relpath(root=self.data_dir)
            item["checksum"] = file.checksum

            # Replace values according to the the meta_values_map
            for field, values_map in self.meta_values_map.items():
                if item[field] is None:
                    continue
                if type(item[field]) == str:
                    for pattern, target_value in values_map.items():
                        matches = re.match(pattern, item[field])
                        if matches:
                            item[field] = target_value
                else:
                    raise NotImplemented('Only strings are currently supported')
            
            # Finally apply individual corrections
            for pattern, corrections in self.corrections.items():
                if re.match(pattern, id):
                    for field, value in corrections.items():
                        item[field] = value

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

def list_datasets():
    return _DATASET_IDS

def is_dataset(dataset_id):
    return dataset_id in _DATASET_IDS

def load_dataset_options(dataset_id):
    cur_dir = os.path.dirname(__file__)
    options_fn = os.path.join(cur_dir, 'options', f'{dataset_id}.json')
    if os.path.exists(options_fn):
        with open(options_fn, 'r') as handle:
            options = json.load(handle)
            return options
    else:
        raise FileNotFoundError(f'Options file for {dataset_id} could not be found')

def get_dataset(dataset_id, data_dir, index_dir):
    if not is_dataset(dataset_id):
        raise ValueError('Invalid dataset id')
    data_dir = os.path.join(data_dir, dataset_id)
    index_path = os.path.join(index_dir, f'{dataset_id}-index.csv')
    props_path = os.path.join(index_dir, f'{dataset_id}-properties.json')
    options = load_dataset_options(dataset_id)
    dataset = Dataset(data_dir, index_path, props_path, **options)
    return dataset

if __name__ == '__main__':
    cur_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(cur_dir, os.path.pardir))
    index_dir = os.path.join(root_dir, 'website', '_data')
    data_dir = os.path.join(root_dir, 'datasets')

    # d = get_dataset('densmore-teton-sioux', data_dir, index_dir)
    # d.save_index()
    # d.save_properties()

    d2 = get_dataset('sagrillo-luxembourg', data_dir, index_dir)
    d2.save_index()
    d2.save_properties()