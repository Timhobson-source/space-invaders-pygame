import yaml
from functools import lru_cache


@lru_cache  # cache means can't change config file mid game (which is ok)
def get_config():
    with open('config/conf.yaml') as f:
        config = yaml.safe_load(f)
    return config
