# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# -------------------------------------------------------------------
"""Some useful utilities"""

import hashlib

def file_checksum(path: str):
    """Return an md5 checksum of a given file

    >>> path = 'tests/datasets/bronson-child-ballads/data/child01.krn'
    >>> file_checksum(path)
    '350fc2b9839d7d7669d83f77efdc03c2'
    
    Parameters
    ----------
    path : str
        The filepath
    
    Returns
    -------
    str
        A md5 checksum of the file
    """
    with open(path, "rb") as handle:
        iterable = iter(lambda: handle.read(4096), b"")
        checksum = checksum_iterable(iterable)
    return checksum

def checksum_iterable(iterable):
    """Return an md5 checksum of an iterable

    >>> checksum_iterable(['hello', 'world'])
    'fc5e038d38a57032085441e7fe7010b0'
    
    Parameters
    ----------
    iterable : iterable
        An iterable of strings or byte-likes
    
    Returns
    -------
    str
        An md5 checksum of the iterable
    """
    hash_md5 = hashlib.md5()
    for chunk in iterable:
        if type(chunk) != bytes: 
            chunk = chunk.encode('utf-8')
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == '__main__':
    import doctest
    doctest.testmod()