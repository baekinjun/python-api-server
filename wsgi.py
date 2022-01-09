import gevent.monkey

gevent.monkey.patch_all()

from management import create_app
from core.handler.response_handler import ResponseHandler
from flask import request
from http import HTTPStatus
from core.config import ENV

app = create_app()


@app.before_request
def check_header():
    GEO_LOCATION = request.headers.get('X-Client-Geo-Location')
    if ENV == "LIVE":
        if GEO_LOCATION == None:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).response()
