# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
"""An index bundles data from various sources. This module implements
various classes that can pull data from different types of sources, 
such as CSV files or a collection of other files. They can then export
the data they have collected as dataframes, which the index finally
combines.

All classes inherit from :class:`BaseSource`. The simplest source is
:class:`Source`, which collects the data you pass to it directly 
during initialization. It is basically a wrapper around some data:

>>> entries = [{'id': 'entry1', 'value': 10}, {'id': 'entry2', 'value': 20}]
>>> source = Source(entries, name='mysource')
>>> source
<Source name=mysource>
>>> type(source.data)
<class 'pandas.core.frame.DataFrame'>

IDs and field names
---------------------

Every entry in a source nees a unique id. The parameter `id_field`
specifies which field  is used as the id:

>>> entries = [{'foo': 'entry1', 'value': 10}, {'foo': 'entry2', 'value': 20}]
>>> source = Source(entries, name='mysource', id_field='foo')
>>> source.data.index.to_list()
['entry1', 'entry2']
>>> source.data.index.name
'cf_id'

Note that the index of the dataframe is named ``cf_id``. Generally, 
all fields that are generated by a source class (and not extracted
from the underlying resource) are given a prefix so that they do 
not clash with fields in the underlying resource. Examples of such 
fields are ``cf_path``, ``cf_checksum`` and ``cf_format``.

ID transformations
---------------------

In some cases you might have to generate an ID field for a, or
transform an existing ID field. For this you can use an ID
transformation. This is a function (or callable) that computes an
ID for an entry based on all the fields of that entry. So it takes
a dictionary describing the entry and outputs a dictionary with 
(at least) an ``id`` field. For example,

>>> entries = [{'foo': 'entry1', 'value': 10}, {'foo': 'entry2', 'value': 20}]
>>> transformer = lambda entry: dict(id=entry['foo'].replace('entry', ''))
>>> transformer({'foo': 'entry1'})
{'id': '1'}
>>> source = Source(entries, name='mysource', id_transformer=transformer)
>>> source.data.index.to_list()
['1', '2']

You can use a :class:`catafolk.transformer.Transformer` for this:

>>> from catafolk.transformer import Transformer
>>> transformer = Transformer([['replace', 'foo', 'id', {'old': 'entry', 'new': ''}]])
>>> entries = [{'foo': 'entry1', 'value': 10}, {'foo': 'entry2', 'value': 20}]
>>> source = Source(entries, name='mysource', id_transformer=transformer)
>>> source.data.index.to_list()
['1', '2']
"""
import os
import glob
import logging
import warnings
import pandas as pd

from .transformer import Transformer
from .file import get_file

__all__ = ['BaseSource', 'Source', 'CSVSource', 'FileSource']

class BaseSource:
    """Base class for data sources.
    
    Parameters
    ----------
    name : str
        A unique name for the data source
    id_field : str, optional
        The name of the field to use as the index. 
        By default ``'id'``.
    id_transformer : callable, optional
        A callable that takes a dictionary with all data for an 
        entry as input, and returns a dictionary with (at least)
        an ``id`` field. This is used as the id for that entry.
    internal_fields_prefix : str, optional
        The prefix used for all fields added by the source class.
        By default ``'cf_'``.
    """
    
    def __init__(self, name = None, id_field = 'id',
        id_transformer = None, 
        internal_fields_prefix: str = 'cf_'):
        if name is None:
            raise ValueError('The argument `name` is required.')

        if id_field is None and id_transformer is None:
            raise ValueError('You have to specify either the '
                '`id_field` or the `id_transformer`')
        
        if (id_transformer is not None 
            and not callable(id_transformer)):
            raise ValueError('The `id_transformer` should be'
                'callable.')
        
        self.name = name
        self.id_field = id_field
        self.id_transformer = id_transformer
        self.internal_fields_prefix = internal_fields_prefix
        self._data = None

    def __repr__(self):
        """String representation of the source"""
        return f'<{self.__class__.__name__} name={self.name}>'

    @property
    def data(self):
        """A dataframe containing all data that has been extracted 
        from the source."""
        if self._data is None:
            df = self._collect()
            self._data = self._set_index(df)
            self._data.sort_index(inplace=True)
        return self._data

    def _collect(self):
        """Private method for collecting the data, implemented in 
        child classes.
        
        The method collects the data as a raw dataframe. The 
        dataframe should *not* have an index column: the index is
        created when exporting the source.
        
        Rturns
        ------
        pd.DataFrame
            A dataframe with all data
        """
        raise NotImplemented

    def _set_index(self, df):
        """Set up the index column of the dataframe. This can either
        be an existing column, or a column obtained by transforming
        some other columns.
        
        Returns
        -------
        pd.DataFrame
            The data from the source
        """
        index = []
        if self.id_transformer is not None:
            for _, row in df.iterrows():
                inputs = row.to_dict()
                outputs = self.id_transformer(inputs)
                if not 'id' in outputs:
                    msg = 'ID transformation failed: no `id` in output.'
                    raise ValueError(msg)
                index.append(outputs['id'])
        elif self.id_field not in df.columns:
            msg = f'ID field {self.id_field} does not exist'
            raise ValueError(msg)
        else:
            index = df[self.id_field]
        
        new_id_field = f'{self.internal_fields_prefix}id'
        df[new_id_field] = index
        df.set_index(new_id_field, inplace=True) 
        return df

class Source(BaseSource):
    """A source wrapping an iterable

    >>> entries = [{'foo': 'entry1', 'value': 10}, {'foo': 'entry2', 'value': 20}]
    >>> source = Source(entries, name='mysource', id_field='foo')
    >>> source.data.index.to_list()
    ['entry1', 'entry2']
        
    Parameters
    ----------
    entries : iterable
        The data, something that can be turned into a pandas
        dataframe.
    """
    def __init__(self, entries, **kwargs):
        super().__init__(**kwargs)
        self.entries = entries
    
    def _collect(self):
        return pd.DataFrame(list(self.entries))

class CSVSource(BaseSource):
    """Load data from a CSV file.

    >>> path = 'tests/test_csv_source.csv'
    >>> source = CSVSource(path, name='csv', id_field='item_id')
    >>> source.data.index.to_list()
    ['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9']
    
    Parameters
    ----------
    path : str
        The path to the csv file
    """

    def __init__(self, path, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    def _collect(self):
        return pd.read_csv(self.path)

class FileSource(BaseSource):
    """Loads data from a collection of files, specified
    by a glob pattern. 

    >>> data_dir = 'tests/datasets/bronson-child-ballads/data'
    >>> pattern = '*.krn'
    >>> source = FileSource(data_dir, pattern, name='file')
    >>> source.data.index.to_list()
    ['child01', 'child02', 'child03', 'child04', 'child05', 'child06', 'child07', 'child09', 'child10']
    
    Parameters
    ----------
    data_dir : str
        The data directory path
    file_pattern : str
        The glob pattern relative to the ``data_dir``
    file_options : dict, optional
        Options passed to :func:`catafolk.file.get_file`.
    use_filename_as_id : bool, optional
        Whether to use the filename as the id, by default True
    **kwargs
        Optional keyword arguments passed to :class:`BaseSource`.
    """
    def __init__(self, data_dir, file_pattern, file_options={},
        use_filename_as_id=True, **kwargs):
        super().__init__(**kwargs)

        # Change id field if using the filename as id
        if use_filename_as_id:
            self.id_field = f'{self.internal_fields_prefix}name'

        # Set up file structure
        self.filepaths = glob.glob(os.path.join(data_dir, file_pattern))
        if len(self.filepaths) == 0: 
            warnings.warn('No files were found')
        self._files = {}
        self.file_options = file_options
        self.data_dir = data_dir      

    @property
    def files(self):
        if len(self._files) == 0:
            for path in self.filepaths:
                file = get_file(path, **self.file_options)
                self._files[path] = file
        return self._files

    def _collect(self):
        entries = []
        prefix = self.internal_fields_prefix
        for path, file in self.files.items():
            entry = file.metadata
            entry[f'{prefix}path'] = file.relpath(self.data_dir)
            entry[f'{prefix}checksum'] = file.checksum
            entry[f'{prefix}format'] = file.format
            entry[f'{prefix}name'] = file.name
            entries.append(file.metadata)
        return pd.DataFrame(entries)

if __name__ == '__main__':
    import doctest
    doctest.testmod()