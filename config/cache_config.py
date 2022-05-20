from typing import List

from apis.api_have_cache import find_all, find_by_id


def api_used_cache() -> List[dict]:
    return [
        {
            'table': 'todos',
            'api': [
                find_all.__name__,
                find_by_id.__name__
            ]
        },
        {
            'table': 'posts',
            'api': [

            ]
        }
    ]
