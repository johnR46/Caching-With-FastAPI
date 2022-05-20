from fastapi import FastAPI

import api_have_cache
import api_with_out_cache
import clear_cache

app = FastAPI()

app.include_router(router=api_with_out_cache.router, prefix="/api/v1")
app.include_router(router=api_have_cache.router, prefix="/api/v2")
app.include_router(router=clear_cache.router, prefix="/api/v2")
