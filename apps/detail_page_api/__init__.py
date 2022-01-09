from flask import Blueprint, request
from flask_restful import Api
from .urls import url_patterns
from .service import AfterService

detail_api = Blueprint('detail_api', __name__, url_prefix='/api_v1/detail')
api = Api(detail_api)

for vi_func, route in url_patterns:
    api.add_resource(vi_func, route)


@detail_api.after_request
def after_request_list(response):
    if request.endpoint == 'detail_api.detailchartview':
        AfterService().up_view_cnt(request)
    return response
