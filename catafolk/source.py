# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
"""Various source classes"""
import glob
import logging
import pandas as pd

from .transformer import Transformer
from .file import get_file

__all__ = ['Source', 'IterableSource', 'CSVSource', 'FileSource']

class Source:
    def __init__(self, name=None, id_field='id', id_transformations=[]):
        """A data source collecting data into a dataframe.

        Correcting different ids
        ------------------------
        Sometimes different source use different ids. You can 
        correct this using an id transformation. The following turns
        an integer `song_no` into an id of the form `ID004`:
    
        ```python
        id_transformations = [
            ["format", "song_no", "id", {"pattern": "ID{:0>3}"}]
        ]
        ```
        
        Parameters
        ----------
        name : string
            A unique name for the data source
        id_field : str, optional
            The name of the id field, by default 'id'
        id_transformations : list, optional
            A list of transformation (shorthands) to transform
            the `id_field` values into the `id` exported by the source.
            By default []
        """
        if name is None:
            raise ValueError('The parameter `name` is required.')
        self.name = name
        self.id_field = id_field
        self.id_transformer = None
        self._data = None
        if len(id_transformations) > 0:
            self.id_transformer = Transformer(id_transformations)

    @property
    def data(self):
        if self._data is None:
            self._data = self._collect_data()
        return self._data

    def _collect_data(self):
        raise NotImplemented

    def collect(self):
        """Return a DataFrame with all data from the source.

        The dataframe is indexed by a `id` column whose value
        can be computed from another field using a transformation.
        
        Returns
        -------
        pd.DataFrame
            The data from the source
        """
        df = self.data.copy()

        # Set up the right id, transorming the id_field if needed.
        if self.id_transformer is None:
            if self.id_field != 'id':
                df['id'] = df[self.id_field]
        else:
            ids = []
            for _, row in df.iterrows():
                raw_id = row[self.id_field]
                inputs = row.to_dict()
                outputs = self.id_transformer(inputs)
                if not 'id' in outputs:
                    raise Exception('ID transformation failed: no `id` in output.')
                ids.append(outputs['id'])
            df['id'] = ids

        df.set_index('id', inplace=True) 
        return df

class IterableSource(Source):
    def __init__(self, entries, **kwargs):
        super().__init__(**kwargs)
        self.entries = entries
    
    def _collect_data(self):
        return pd.DataFrame(list(self.entries))

class CSVSource(Source):
    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    def _collect_data(self):
        return pd.read_csv(self.path)

class FileSource(Source):

    def __init__(self, data_dir, glob_pattern, options={}, **kwargs):
        super().__init__(**kwargs)
        self.filepaths = glob.glob(glob_pattern)
        self.data_dir = data_dir
        self.options = options
        self._files = {}

    @property
    def files(self):
        if len(self._files) == 0:
            for path in self.filepaths:
                file = get_file(path, **self.options)
                self._files[path] = file
        if len(self._files) == 0:
            warnings.warn('No files were found!')
        return self._files

    def _collect_data(self):
        entries = []
        for path, file in self.files.items():
            entry = file.metadata
            entry['cf_path'] = file.relpath(self.data_dir)
            entry['cf_checksum'] = file.checksum
            entry['cf_format'] = file.format
            entries.append(file.metadata)
        return pd.DataFrame(entries)