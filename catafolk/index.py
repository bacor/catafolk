import os
import pandas as pd
import logging
from catafolk.transformer import Transformer

class Source():
    def __init__(self, name, entries=None, id_field='id',
        id_transformations=[]):
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
        entries : iterable, optional
            An optional iterable of entries, which can be turned
            into a DataFrame. By default None
        id_field : str, optional
            The name of the id field, by default 'id'
        id_transformations : list, optional
            A list of transformation (shorthands) to transform
            the `id_field` values into the `id` exported by the source.
            By default []
        """
        self.name = name
        self.id_field = id_field
        self.id_transformer = None
        if len(id_transformations) > 0:
            self.id_transformer = Transformer(id_transformations)
        if entries:
            self.entries = list(entries)

    def collect(self):
        """Return a DataFrame with all data from the source.

        The dataframe is indexed by a `id` column whose value
        can be computed from another field using a transformation.
        
        Returns
        -------
        pd.DataFrame
            The data from the source
        """
        df = pd.DataFrame(self.entries)

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

class CSVSource(Source):
    def __init__(self, name, path, **kwargs):
        super().__init__(name, **kwargs)
        self.entries = pd.read_csv(path)

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
        
    

