import appdirs
import yaml
import os
from pathlib import Path
from typing import Optional

APPNAME = 'Catafolk'
APPAUTHOR = 'Catafolk'

class CatafolkConfig:

    version_ = '0.0.1'

    def __init__(self, config_dir: Optional[str] = None, **kwargs):
        # Default configuration
        self.default_config_ = dict(
            version=self.version_,
            data_dir=appdirs.user_data_dir(APPNAME, APPAUTHOR)
        )

        # Load the configuration file, or create one if none exists
        if config_dir is None:
            config_dir = appdirs.user_config_dir(APPNAME, APPAUTHOR)
        self.config_path = Path(config_dir, 'config.yml')
        self.config = dict()
        if self.config_path.exists():
            self.load()
            self.update(**kwargs)
        else:
            config = dict()
            config.update(self.default_config_)
            config.update(kwargs)
            self.update(**config)
        print(self.config)

    def get(self, key: str): 
        if key in self.default_config_.keys():
            return self.config[key]
        else:
            raise KeyError(f'Key {key} is not supported.')
        
    def save(self):
        if not self.config_path.parent.exists():
            self.config_path.parent.mkdir(parents=True)

        with open(self.config_path, 'w') as stream:
            yaml.safe_dump(self.config, stream)

    def load(self):
        if self.config_path.exists():
            with open(self.config_path, 'r') as stream:
                self.config = yaml.safe_load(stream)

    def update(self, **kwargs):
        for key in list(kwargs.keys()):
            if key not in self.default_config_.keys():
                del kwargs[key]
        self.config.update(kwargs)
        self.save()

    def reset(self):
        self.update(**self.default_config_)   


if __name__ is '__main__':
    c = CatafolkConfig()
    print(c)