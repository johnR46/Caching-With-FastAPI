import hashlib
import json
import logging
import time
from typing import Optional

from pymemcache.client import base

logging.basicConfig(level=logging.INFO)

client = base.Client(('localhost', 11211))


def get_value_from_cache(key: str):
    cache_value = client.get(key)
    if cache_value is None:
        return None
    return json.loads(cache_value)


def set_value_to_cache(key: str, value: any) -> None:
    logging.info(f"set_value_to_cache:'{key}'")
    client.set(key, json.dumps(value), expire=60 * 60 * 24 * 7)


def delete_cached(key_list: list):
    for key in key_list:
        client.delete(key)
        logging.info(f"cache key '{key}' deleted")
        time.sleep(0.2)


def default_key_builder(prefix: str, parameter: Optional[dict] = None) -> str:
    cache_key = prefix + ':' + hashlib.md5(f"{parameter}".encode()).hexdigest()
    return cache_key
