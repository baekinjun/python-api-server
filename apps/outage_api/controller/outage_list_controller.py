# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from flasgger import swag_from

# 커스텀 코드
from ..service import OutageListService
from core.handler import ResponseHandler
from ..dto import *


class OutageListView(Resource):
    def __init__(self):
        self.outage_page_service = OutageListService()

    def get(self):
        try:
            outage = OutageListModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.outage_page_service.outage_list(outage.period, outage.start_page, outage.per_page,
                                                       outage.company_id)
        except Exception as e:
            return ResponseHandler(HTTPStatus.INTERNAL_SERVER_ERROR).response()

        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"


class OutageSearchListView(Resource):
    def __init__(self):
        self.outage_page_service = OutageListService()

    def get(self):
        try:
            s_outage = OutageSearchListModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.outage_page_service.outage_search(s_outage.period, s_outage.search_keyword, s_outage.start_page,
                                                         s_outage.per_page)
            if res == None:
                return ResponseHandler(HTTPStatus.NO_CONTENT).response()
        except Exception as e:
            return ResponseHandler(HTTPStatus.BAD_REQUEST).response()
        return ResponseHandler(HTTPStatus.OK).payload(res)


class MonthDataView(Resource):
    def __init__(self):
        self.outage_page_service = OutageListService()

    def get(self):
        try:
            now = MonthModel(**request.args.to_dict()).now
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        month_list = self.outage_page_service.monthly_data(now)
        return ResponseHandler(HTTPStatus.OK).payload(month_list)

    def post(self):
        return "This endpoint does not exist. Please check!"
