import configparser
from functools import lru_cache
import os

config = configparser.ConfigParser()
config.read(os.path.abspath('..\\config.ini'))

@lru_cache
def get_property(family,property_name):
    return config[family][property_name]
