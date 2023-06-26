# by: KishinNext
#    /\
#   /  \__
#  (     @\____
#   /          O
#  /    (_____/
# /_____/   U

import logging
import logging.config

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from routers import slack
from utils.config_loaders import (
    get_config,
    setup_logging
)

config = get_config()
setup_logging(config)

api = FastAPI(
    title='Slack Bot - API',
    docs_url="/docs",
    openapi_url="/openapi.json"
)

api.include_router(
    slack.router,
    prefix='/slack',
    tags=['slack']
)


@api.get('/ping')
def health_check():
    """Health check endpoint. Returns the status of the API.

    Returns:
        dict: The status of the API.
    """
    return {
        'health': 'OK'
    }


@api.get('/version')
def version():
    """Version endpoint. Returns the current version of the API.

    Returns:
        dict: The current version of the API.
    """
    return {
        'api_version': 0.1
    }


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Handles validation errors for requests.

    Args:
        request: The request that caused the validation error.
        exc: The exception raised.

    Returns:
        JSONResponse: The response containing the error details.
    """
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {
        'status_code': 422,
        'message': exc_str,
        'data': None
    }
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == "__main__":
    # use this for local development, replace localhost for the database host
    uvicorn.run("app:api", host="0.0.0.0", port=8080, log_level="info", reload=True)
