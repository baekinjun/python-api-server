# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from flasgger import swag_from

# 커스텀 코드
from core.handler import ResponseHandler
from apps.main_page_api.service import MainRecentOutageService
from apps.main_page_api.dto import *


class RecentAsnOutageView(Resource):
    def __init__(self):
        self.main_page_service = MainRecentOutageService()

    def get(self):
        try:
            statics = StaticsModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.main_page_service.recent_asn_outage(statics.now, statics.date_type)
        return ResponseHandler(HTTPStatus.OK).payload(res)


class RecentServerOutageView(Resource):
    def __init__(self):
        self.main_page_service = MainRecentOutageService()

    def get(self):
        try:
            statics = StaticsModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.main_page_service.recent_server_outage(statics.now, statics.date_type)
        return ResponseHandler(HTTPStatus.OK).payload(res)


class RecentOutageInfoChartView(Resource):
    def __init__(self):
        self.main_page_service = MainRecentOutageService()

    def get(self):
        res = self.main_page_service.recent_outage_info()
        return ResponseHandler(HTTPStatus.OK).payload(res)
