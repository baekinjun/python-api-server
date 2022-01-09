# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from flasgger import swag_from

# 커스텀 코드
from ..service import OutageDetailService
from core.handler import ResponseHandler
from ..dto import *


class DetailOutageInfoView(Resource):
    def __init__(self):
        self.outage_page_service = OutageDetailService()

    def get(self):
        try:
            outage = DetailOutageModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        try:
            res = self.outage_page_service.detail_outage(**outage.dict())
        except Exception as e:
            return ResponseHandler(HTTPStatus.INTERNAL_SERVER_ERROR).response()
        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"


class DetailOutageChartView(Resource):
    def __init__(self):
        self.outage_page_service = OutageDetailService()

    def get(self):
        try:
            outage = DetailOutageModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        try:
            res = self.outage_page_service.detail_chart_array(**outage.dict())
        except Exception as e:
            return ResponseHandler(HTTPStatus.INTERNAL_SERVER_ERROR).response()
        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"
