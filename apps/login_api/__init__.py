from flask import Blueprint, request
from flask_restful import Api
from .urls import url_patterns

auth_api = Blueprint('auth_api', __name__, url_prefix='/api_v1/auth')
api = Api(auth_api)

for vi_func, route in url_patterns:
    api.add_resource(vi_func, route)
