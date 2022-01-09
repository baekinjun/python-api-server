from flask import Blueprint, request
from flask_restful import Api
from .urls import url_patterns
from core.handler.response_handler import ResponseHandler
from core.config import fake_key
from http import HTTPStatus

#
admin_api = Blueprint('admin_api', __name__, url_prefix='/api_v1/admin')
api = Api(admin_api)

for vi_func, route in url_patterns:
    api.add_resource(vi_func, route)


@admin_api.before_request
def auth():
    if request.headers.get('X-Api-Key') != fake_key:
        return ResponseHandler(HTTPStatus.UNAUTHORIZED).response()
