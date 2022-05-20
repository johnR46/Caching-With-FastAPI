import logging

from fastapi import APIRouter, HTTPException

from config.cache_config import api_used_cache
from utils.cache_util import delete_cached
from utils.memcache_status import MemcachedStats

logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/clear-cache",
    tags=["clear Cache"],
    responses={404: {"message": "Not found"}}
)


@router.post("/{table_name}")
async def clear_cache(table_name: str):
    return clear_cache_by_table_name(table_name)


def clear_cache_by_table_name(table_name: str):
    # check table available
    conf_used_cache = api_used_cache()
    check_table_available = [x for x in conf_used_cache if x.get('table') == table_name]
    if len(check_table_available) <= 0:
        raise HTTPException(
            status_code=404,
            detail=f'table:{table_name} not found'
        )

    # get prefix api
    prefix_api_used_cache_by_table = [x.get('api') for x in check_table_available][0]
    logging.info(f'prefix api:{prefix_api_used_cache_by_table}')

    # get all key from memcache
    memcache = MemcachedStats(host='localhost', port=11211)
    cache_keys = list(set(memcache.keys()))
    logging.info(f'cache_keys:{cache_keys}')

    # get match key by cache_keys start with prefix_api
    cache_key_for_delete = [x for x in cache_keys if x.startswith(tuple(prefix_api_used_cache_by_table))]

    # delete cache by keys
    delete_cached(cache_key_for_delete)
    return {"Status": "Success"}
