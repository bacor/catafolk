import os
import hashlib
import re

# Map of extensions to file formats
_EXTENSIONS = dict(krn='kern')

_SUPPORTED_FILE_FORMATS = ['kern']

def is_supported_format(format):
    return format in _SUPPORTED_FILE_FORMATS

class File(object):
    format = None
    
    def __init__(self, filepath, encoding='utf-8'):
        self.path = filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError()
        self.encoding = encoding
        filename = os.path.basename(self.path)
        self.id = os.path.splitext(filename)[0]

        self._metadata = None
        self._checksum = None

    def extract_metadata(self):
        raise NotImplemented()

    @property
    def metadata(self):
        if self._metadata is None:
            self._metadata = self.extract_metadata()
        return self._metadata

    @property
    def checksum(self):
        if self._checksum is None:
            # https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
            hash_md5 = hashlib.md5()
            with open(self.path, "rb") as handle:
                for chunk in iter(lambda: handle.read(4096), b""):
                    hash_md5.update(chunk)
            self._checksum = hash_md5.hexdigest()
        return self._checksum

    def relpath(self, root):
        return os.path.relpath(self.path, start=root)

class KernFile(File):
    format = 'kern'

    def extract_metadata(self):
        """Extract metadata from a kern file.
        The function looks for lines of the form `!!![key]: [value]`, and puts
        those in a Python dictionary
        
        Arguments:
            filename {string} -- filename
        
        Returns:
            dict -- A dictionary of metadata.
        """
        metadata = {}
        with open(self.path, 'r', encoding=self.encoding) as handle:
            for line in handle:
                match = re.match(r'^\!{3}([^:]+): (.+)', line)
                if match:
                    key = match[1]
                    value = match[2]
                    metadata[key] = value
        return metadata

def get_file(filepath, format='infer', **kwargs):
    """File factory function that returns a File instance with the right format"""
    if format == 'infer':
        _, ext = os.path.splitext(filepath)
        format = _EXTENSIONS.get(ext[1:])
    
    if format == 'kern':
        return KernFile(filepath, **kwargs)
    else:
        raise Exception('Unknown file format')