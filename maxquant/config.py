from typing import Dict

import os
import yaml
from os.path import join, exists


def get_config_path()->str:
    home = os.getenv('HOME')
    return join(home, '.maxquant', 'config.yml')


def read_config(config_path: str=None)->Dict[str, str]:
    config_path = config_path or get_config_path()
    with open(config_path) as f:
        config = yaml.load(f)
        validate_config(config)
        return config


def validate_config(config: Dict[str, str]):
    keys = [
        'maxquant_cmd.bin',
        'database.fasta',
        'mqpar.template',
    ]
    for key in keys:
        if key not in config:
            raise Exception('You must set {} in config'.format(key))
        value = config[key]
        if not exists(value):
            raise Exception('{}: {} does not exist'.format(key, value))