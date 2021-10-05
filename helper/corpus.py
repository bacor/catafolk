import pandas as pd
import os
import warnings
from pathlib import Path
from typing import Iterator, Union
import yaml

from config import CatafolkConfig

from utils import file_checksum

CORPORA = {
    'densmore-pawnee': ['1.0'],
    'densmore-pueblo': ['1.0']
}

def verify_corpus_id(corpus_id: str) -> bool:
    """Verify whether a string is a valid corpus_id. The method checks if the
    corpus_id occurs in the latest release of Catafolk by checking against
    a list of corpus_ids.

    Parameters
    ----------
    corpus_id : str
        The string to be verified

    Returns
    -------
    bool
        True when the input is a valid corpus id, false otherwise.
    """
    return corpus_id in CORPORA.keys()
    
def verify_corpus_version(corpus_id: str, version: str) -> bool:
    """Verify whether a string is a valid version number of a corpus. This is
    verified by comparing the string to a hard-coded list of accepted version
    numbers.

    Parameters
    ----------
    corpus_id : str
        The id of the corpus
    version : str
        The version string to be verified

    Returns
    -------
    bool
        True when the input 
    """
    if not verify_corpus_id(corpus_id):
        raise ValueError(f'Invalid corpus_id "{corpus_id}"')
    
    if version == 'latest':
        return True
    else:
        return version in CORPORA[corpus_id]

class Corpus:
    """A catafolk corpus"""

    def __init__(self, corpus_id: str, version: str = 'latest', 
        config_kws: dict = {},
        safe_mode: bool = True):

        self.config = CatafolkConfig(**config_kws)

        if not verify_corpus_id(corpus_id):
            if safe_mode:
                raise ValueError(f'Invalid corpus_id {corpus_id}')
            else:
                warnings.warn(f'Unknown corpus_id {corpus_id}')

        if not verify_corpus_version(corpus_id, version):
            if safe_mode:
                raise ValueError(
                    f'Invalid version {version} for corpus_id {corpus_id}'
                )
            else:
               warnings.warn(
                    f'Unknown version {version} for corpus_id {corpus_id}'
                )

        if version == 'latest':
            version = CORPORA[corpus_id][-1]

        self.id = corpus_id
        self.version = version
        self.safe_mode = safe_mode
        self.data_dir = self.config.get('data_dir')
        self.root = Path(self.data_dir, corpus_id, version).resolve()

        # Pandas Dataframe with the index
        self.df_ = None

        # Dictionary containing all metadata
        self.meta_ = None

    def __repr__(self):
        return f'<Corpus {self.id} v{self.version}>'

    def path(self, *args: str) -> Path:
        """Return a path object given a string specifying the path. The string
        has to specify a file or directory that is inside the root directory
        of the dataset, or otherwise a ValueError is raised.

        Returns
        -------
        Path
            A path object

        Raises
        ------
        ValueError
            Raised when the passed arguments specify a directory outside the
            root directory of the dataset.
        """
        path = self.root.joinpath(*args).resolve()

        if not path.exists():
            raise Exception(f'The path {str(path)} does not exist')

        if self.root not in path.parents:
            raise ValueError(
                f'The provided path ({str(path)}) is outside the root '
                'directory of this dataset.'
            )
            
        return path

    def download(self):
        raise NotImplemented()
    
    def verify(self) -> bool:
        """Verifies the corpus. It checks whether all the checksums of all files
        in the corpus match the checksum listed in the index. If the checksums
        don't match, a warning is issued.

        Returns
        -------
        bool
            True if the corpus is succesfully verified, False otherwise.
        """
        for (song_id, row), path in zip(self.index.iterrows(), self.files):
            if not file_checksum(path) == row['checksum']:
                warnings.warn(
                    f'Checksum of {song_id} does not match the checksum in the'
                    'index.'
                )
                return False
        return True
            
    @property
    def index(self) -> pd.DataFrame:
        """An index Dataframe. This is a large table with columns corresponding
        to catafolk characters, and the values for all songs in the dataset. The
        dataframe is loaded from the `index.csv` file in the root directory of 
        the corpus.

        Returns
        -------
        pd.DataFrame
            The index to the corpus
        """
        if self.df_ is None:
            index_fn = self.path('index.csv')
            self.df_ = pd.read_csv(index_fn, index_col=0)
        return self.df_

    @property
    def metadata(self) -> dict:
        """A dictionary with metadata loaded from the `dataset.yml` file in the
        root directory of the corpus.

        Returns
        -------
        dict
            A dictionary with metadata.
        """
        if self.meta_ is None:
            meta_fn = str(self.path('dataset.yml'))
            with open(meta_fn, 'r') as stream:
                self.meta_ = yaml.safe_load(stream)

        return self.meta_
            
    @property
    def files(self) -> Iterator[Union[Path, None]]:
        """An iterable of file paths of all files in the corpus. If a song in 
        the corpus does not have a file (i.e., no path property), the iterable
        contains `None` for that song. 

        Yields
        -------
        Generator[Path, None]
            A generator with paths for each of the songs in the corpus. If a 
            song does not exist, it yields None.

        Raises
        ------
        Exception
            Raised when the corpus contains no files (i.e., the `path` column 
            in the index is empty).
        """
        if pd.isnull(self.index['path']).all():
            raise Exception('This corpus has no files.')

        for path in self.index['path']:
            if pd.notna(path):
                yield self.path(path)
            else:
                yield None

if __name__ == '__main__':
    corpus = Corpus('densmore-pawnee', 
        config_kws=dict(data_dir=str(Path.home() / 'surfdrive' / 'catafolk')))
    corpus.verify()
    print(corpus.files)
    print(corpus)