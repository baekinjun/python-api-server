from flask import Blueprint, request
from flask_restful import Api
from .urls import url_patterns
from .service import AfterService

main_page_api = Blueprint('main_page_api', __name__, url_prefix='/api_v1/main')
api = Api(main_page_api)

for vi_func, route in url_patterns:
    api.add_resource(vi_func, route)


@main_page_api.after_request
def after_request_list(response):
    if request.endpoint == 'main_api.mainchartview':
        AfterService().collect_keyword(request)
    return response


