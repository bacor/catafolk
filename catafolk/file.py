# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
"""Most of the metadata included in Catafolk comes from music files, 
such as kern files. This metadata is extracted by the `File` classes:
there is one for every file format. Currently supported are `kern` 
and `xml`.

Files can be instantiated using :func:`get_file` which automatically
determines the file format based on the extension.

>>> data_dir = 'tests/datasets/bronson-child-ballads/data'
>>> file = get_file(f'{data_dir}/child01.krn')
>>> file
<KernFile name=child01 format=kern>
>>> file.metadata.keys()
dict_keys(['ONM', 'PPG', 'AMT', 'YOR', 'OVM', 'PPE', 'PSR', 'PSP', 'PSD', 'ENC', 'EMD', 'EEV'])
>>> file.metadata['ONM']
'Child Ballad No. 1, Tune No. 1'

Note that metadata is collected only once and then stored internally.
In the code above, we accessed ``file.metadata`` twice, but the file
was only read out once. You can reset the stored metadata using 
:meth:`File.reset`.
"""


import os
import re
import xml.etree.ElementTree as ET
from .utils import file_checksum
# Map of extensions to file formats
_EXTENSIONS = dict(krn='kern', xml='xml')

def get_file(filepath, format='infer', **kwargs):
    """File factory that returns a File instance of the right type
    
    Parameters
    ----------
    filepath : str
        Path to the file
    format : str, optional
        File format. Currently supported are `kern` and `xml`. When
        `format='infer'` the format is inferred from the extension.
        By default 'infer'
    
    Returns
    -------
    File
        The File instance
    """
    if format == 'infer':
        _, ext = os.path.splitext(filepath)
        format = _EXTENSIONS.get(ext[1:])
    if format == 'kern':
        return KernFile(filepath, **kwargs)
    elif format == 'xml':
        return XMLFile(filepath, **kwargs)
    else:
        raise Exception('Unknown file format')

class File:
    """The base class for music files."""

    format = None
    """The file format, e.g. ``'kern'`` or ``'xml'``"""

    #TODO document properties
    
    def __init__(self, filepath, encoding='utf-8'):
        self.path = filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError()

        self.encoding = encoding
        filename = os.path.basename(self.path)
        self.name = os.path.splitext(filename)[0]
        self.reset()

    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name} format={self.format}>'
    
    @property
    def metadata(self):
        """A dictionary with metadata collected from the file.
        Which properties are are included in the metadata depends 
        completely on the contents of the file. Properties like
        the path are *not* included in the metadata.

        Metadata is collected only once, and then stored in the 
        class. You can reset the file using :meth:`reset`."""
        if self._metadata is None:
            self._metadata = self._collect_metadata()
        return self._metadata

    @property
    def checksum(self):
        """An md5 checksum of the file.
        
        >>> file = get_file('tests/datasets/bronson-child-ballads/data/child01.krn')
        >>> file.checksum
        '350fc2b9839d7d7669d83f77efdc03c2'
        """
        if self._checksum is None:
            self._checksum = file_checksum(self.path)
        return self._checksum

    def relpath(self, root):
        """Return the relative path with respect to some
        root directory.

        >>> file = get_file('tests/datasets/bronson-child-ballads/data/child01.krn')
        >>> file.path
        'tests/datasets/bronson-child-ballads/data/child01.krn'
        >>> file.relpath(root='tests/datasets/bronson-child-ballads')
        'data/child01.krn'
        
        Parameters
        ----------
        root : str
            The root directory
        
        Returns
        -------
        str
            The relative path
        """
        return os.path.relpath(self.path, start=root)

    def reset(self):
        """Reset the file instance: remove stored metadata and 
        checksum. This only affects the class instance, the file 
        itself is (as always) left untouched. This might be useful 
        if the file  has changed and you want to refresh the
        metadata."""
        self._metadata = None
        self._checksum = None
    
    def _collect_metadata(self):
        raise NotImplemented()

    def _analyze(self):
        raise NotImplemented()

class KernFile(File):
    """A class for loading ``**kern**`` files.
    
    When extracting metadata, the class looks for kern *reference
    records* of the form ``!!![key]: [value]``. These are collected 
    in a dictionary. If a key is encountered multiple times, all
    values are collected in a list.
    """

    format = 'kern'

    def _collect_metadata(self):
        """Extract metadata from a kern file."""
        metadata = {}
        with open(self.path, 'r', encoding=self.encoding) as handle:
            for line in handle:
                match = re.match(r'^\!{3}([^:]+):[ \t]*(.+)', line)
                if match:
                    key = match[1]
                    value = match[2]
                    # Key `id` is reserved
                    if key == 'id': key = '_id'
                    if key not in metadata:
                        metadata[key] = value
                    elif type(metadata[key]) == list:
                        metadata[key].append(value)
                    else:
                        metadata[key] = [metadata[key], value]
        return metadata

class XMLFile(File):
    format = 'xml'

    def _collect_metadata(self):
        metadata = {}
        root = ET.parse(self.path).getroot()
        meta_containers = ['work', 'identification']
        for container_tag in meta_containers:
            containers = root.iter(container_tag)
            if containers is not None:
                for container in containers:
                    for element in container.iter():
                        if type(element.text) is str and element.text.strip() != '':
                            metadata[element.tag] = element.text
        return metadata

if __name__ == '__main__':
    import doctest
    doctest.testmod()