from flask import Blueprint
from flask_restful import Api
from .urls import url_patterns

outage_api = Blueprint('outage_api', __name__, url_prefix='/api_v1/outage')
api = Api(outage_api)

for vi_func, route in url_patterns:
    api.add_resource(vi_func, route)
