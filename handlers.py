import logging
import time

import starlette.requests
from fastapi import FastAPI
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from apis import api_with_out_cache, api_have_cache, api_clear_cache

logging.basicConfig(level=logging.INFO)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = ["*"]
# origins = ["https://baanbaan.co/", "https://saas.baanbaan.co/", "http://localhost",]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logging.info("Application start")


@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application shutdown")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# handler error HTTP
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: starlette.requests.Request, exc):
    logging.error("request url : {} | {} | {}".format(request.url, exc.status_code, exc.detail))
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "description": exc.detail
        }),
    )


app.include_router(router=api_with_out_cache.router, prefix="/api/v1")
app.include_router(router=api_have_cache.router, prefix="/api/v2")
app.include_router(router=api_clear_cache.router, prefix="/api/v2")
