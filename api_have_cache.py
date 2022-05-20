from fastapi import APIRouter

from cache_util import get_value_from_cache, set_value_to_cache, default_key_builder
from mock_response import get_todo_all, get_todo_by_id

router = APIRouter(
    prefix="/todo",
    tags=["have-cache/todos"],
    responses={404: {"message": "Not found"}}
)


@router.get("/find/all")
async def find_all():
    # prefix
    key = find_all.__name__
    # parameter
    parameter = {}
    key_cache = default_key_builder(key, parameter)
    cache_value = get_value_from_cache(key_cache)

    if cache_value is None:
        response = get_todo_all()
        set_value_to_cache(key_cache, response)
        return response
    else:
        return cache_value


@router.get("/find/{todo_id}")
async def find_by_id(todo_id: int):
    # prefix
    key = find_by_id.__name__
    # parameter
    parameter = {
        "id": todo_id
    }
    key_cache = default_key_builder(key, parameter)
    cache_value = get_value_from_cache(key_cache)

    if cache_value is None:
        response = get_todo_by_id(todo_id)
        set_value_to_cache(key_cache, response)
        return response
    else:
        return cache_value
