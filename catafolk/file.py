import os
import hashlib
import re

# Map of extensions to file formats
_EXTENSIONS = dict(krn='kern')

_SUPPORTED_FILE_FORMATS = ['kern']


_FIELDS = ['id', 'title', 'title_eng', 'location', 'latitude', 'longitude', 
           'culture', 
           'collection_date', 'collector', 'performer'
           'source', 'source_key',
           'source_page_num', 'source_song_num', 'source_date', 'catalogue_number'
           'encoder',
           'encoding_date', 'copyright', 'license_abbr', 'version', 'meter',
           'metric_classification',
           'modality', 'key', 'ambitus', 'has_lyrics', 'has_music', 
           'genre', 'language', 'language_iso', 
           'url', 'preview_url', 'path', 'format', 'checksum']

def convert_meta_fields(metadata, conversion): 
    out = {}
    for orig_field, converter in conversion.items():
        if orig_field not in metadata: 
            continue
        
        elif type(converter) == str:
            new_field = converter
            out[new_field] = metadata[orig_field]

        elif type(converter) == list:
            for new_field in converter:
                out[new_field] = metadata[orig_field]
        
        elif type(converter) == dict and converter['type'] == 'regex':
            orig_value = metadata[orig_field]
            matches = re.match(converter['pattern'], orig_value)
            if matches:
                for group_num, new_field in enumerate(converter['groups']):
                    if new_field is not None and matches[group_num + 1] is not None:
                        new_value = matches[group_num + 1] 
                        if 'lowercase' in converter:
                            new_value = new_value.lower()
                        out[new_field] = new_value

            elif "default" in converter:
                new_field = converter["default"]
                new_value = orig_value
                if 'lowercase' in converter:
                    new_value = new_value.lower()
                out[new_field] = orig_value
            
        else:
            raise ValueError('Invalid conversion')
    
    return out

def convert_meta_values(metadata, conversion):
    for field, converter in conversion.items():
        if metadata[field] is None:
            continue

        elif converter['type'] == 'regex':
            found_match = False
            for pattern, target_value in converter['map'].items():
                matches = re.match(pattern, metadata[field])
                if matches:
                    if type(target_value) == str:
                        metadata[field] = target_value.format(**metadata)
                    else:
                        metadata[field] = target_value
                    found_match = True
                    break
            if not found_match and 'default_null' in converter:
                metadata[field] = None
        
        elif converter['type'] == 'dtype':
            if converter['dtype'] == 'int':
                try:
                    metadata[field] = int(metadata[field])
                except:
                    pass
        else:
            raise NotImplemented()

    return metadata

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

    def read_metadata(self):
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

    def export(self, 
        default_field_values={},
        override_field_values={},
        meta_fields_conversion={}, 
        meta_values_conversion={}, 
        data_dir=None, 
        corrections={}):
        """Export the file to a dictionary with all fields in the index.
        The values are extracted from the metadata using various conversions
        
        Parameters
        ----------
        default_field_values : dictionary, optional
            The default values for each of the fields. These values are
            set before any of the conversions and might be overriden.
            By default {}
        override_field_values : dict, optional
            Values to be overridden, by default {}
        meta_fields_conversion : dict, optional
            A dictionary with a converters for each field in the original metadata.
            Here is an example with converters for the fields `OTL` and `reg`:
            ```
            meta_fields_conversion = {
                "OTL": {
                    "type": "regex",
                    "pattern": "(.*), S. (\\d+)?",
                    "groups": [null, "title", "source_song_num"],
                    "default": "title"
                },
                "reg": "location"
            }
            ```
            The first converter describes how to convert the string in the metadata 
            field `OTL`.It specifies a regular expression `pattern` that is used 
            to extract two substrings (groups), which are then stored in the `title` 
            and `source_song_num` field. In this way, you can extract multiple fields
            from a single field in the original metadata.

            The second converter takes the value `reg` in the original metadata
            and stores it in the `location` field. It basically renames the metadata.
            
            By default {}
        meta_values_conversion : dict, optional
            Similar to the meta_fields_conversion option, this is a dictionary 
            describing how to convert certain meta *values*. Typically, it is used
            to convert references to bibtex keys.
            ```
            "meta_values_conversion": {
                "source_key": {
                    "type": "regex",
                    "map": {
                        "Some folksongs, France, 1935": "mybibtexkey",
                        ...
                    },
                    "default_null": true
                },
                "source_song_num": {
                    "type": "dtype",
                    "dtype": "int"
                }
            },
            ```
            The first converter operates on the `source_key` field, checks whether
            it matches (as a regex) one of the keys in the dictionary `map`, and if so,
            replaces it by the value `mybibtexkey`.
            
            The second converter convertes the value of `source_song_num` into an integer.
            
            By default {}
        data_dir : [type], optional
            [description], by default None
        corrections : dict, optional
            Individual corrections
            [description], by default {}
        
        Returns
        -------
        dict
            A dictionary with values for all fields.
        """
        # Empty item with all fields
        item = { field: None for field in _FIELDS}
        
        # Update with default values
        item.update(default_field_values)

        # Update with converted metadata
        metadata = convert_meta_fields(self.metadata, meta_fields_conversion)
        item.update(metadata)

        # Set automatically computed fields
        item["id"] = self.id
        item["format"] = self.format
        item["path"] = self.relpath(root=data_dir)
        item["checksum"] = self.checksum

        # Override field values
        for field, value in override_field_values.items():
            item[field] = value.format(**item)

        # Replace values according to the the meta_values_map
        item = convert_meta_values(item, meta_values_conversion)
        
        # Finally apply individual corrections
        for pattern, corrections in corrections.items():
            if re.match(pattern, self.id):
                for field, value in corrections.items():
                    item[field] = value
         
        return item

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
        # TODO Duplicate keys are common in KERN files...
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