# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
import os
import pandas as pd
import logging

from .source import *

class Index():
    def __init__(self, path, fields=[], transformer=None):
        self.path = path
        self.transformer = transformer
        self.fields = fields
        if 'id' not in fields:
            self.fields = ['id'] + fields

        self._sources = {}
        self._data = None

    @property
    def sources(self):
        if len(self._sources) == 0:
            raise Exception('No sources have been registered')
        else:
            return self._sources
    
    @property
    def has_file(self):
        return os.path.exists(self.path)

    @property
    def data(self):
        if self._data is None:
            if self.has_file:
                self.load()
            else:
                self.initialize()
        return self._data

    def register_sources(self, *sources):
        for source in sources:
            assert isinstance(source, Source)
            self._sources[source.name] = source

    def initialize(self):
        self._data = pd.DataFrame([], columns=self.fields)
        self._data.set_index('id', inplace=True)
    
    def load(self):
        if os.path.exists(self.path):
            self._data = pd.read_csv(self.path, index_col='id')
        else:
            raise FileNotFoundError('Index file does not exist. Update the index.') 

    def save(self):
        self.data.to_csv(self.path, index=True)
    
    def clear(self):
        if self.has_file:
            os.remove(self.path)
        self._data = None

    def update(self, df, **kwargs):
        columns = [col for col in df.columns if col in self.fields]
        subset = df[columns]

        updates = subset.index.intersection(self.data.index)
        self.data.update(subset.loc[updates, :])

        new_entries = subset.index.difference(self.data.index)
        self._data = self.data.append(subset.loc[new_entries,:])

    def collect(self, fields=None):
        dataframes = []
        columns = []
        for name, source in self.sources.items():
            source_df = source.collect()
            if name != '':
                columns.extend([f'{name}.{col}' for col in source_df.columns])
            else:
                columns.extend(source_df.columns)
            dataframes.append(source_df)
        df = pd.concat(dataframes, axis=1, join='outer')
        df.columns = columns
        df.index.name = 'id'
        return df

    def transform(self, df):
        if self.transformer is None:
            logging.warn('This index has no transformer; returning dataframe')
            return df

        transformed_entries = []
        for entry_id, row in df.iterrows():
            entry = row.to_dict()
            entry['id'] = entry_id
            transformed = self.transformer(entry, outputs_only=False)
            transformed['id'] = entry_id
            transformed_entries.append(transformed)
        transformed_df = pd.DataFrame(transformed_entries).set_index('id')
        return transformed_df

    def make(self):
        data = self.collect()
        logging.info(f'Collected {len(data.columns)} columns:')
        logging.info(list(data.columns))
        transformed_data = self.transform(data)
        self.update(transformed_data)
        self.save()
        
    

