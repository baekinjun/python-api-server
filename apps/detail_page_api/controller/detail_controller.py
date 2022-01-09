# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from flasgger import swag_from

# 커스텀 코드
from core.handler import ResponseHandler
from apps.detail_page_api.service import DetailPageService
from apps.detail_page_api.dto import *

# 서드파티
from apps.middleware import cache

# 캐시키 규칙
from apps.detail_page_api.detail_cache import detail_chart_cache, detail_info_cache


class BaseLineView(Resource):
    def __init__(self):
        self.detail_page_service = DetailPageService()

    def get(self):
        try:
            baseline = BaseLineModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.detail_page_service.baseline(baseline.now, baseline.company_id)
        return ResponseHandler(HTTPStatus.OK).payload(res)


class DetailInfoView(Resource):
    def __init__(self):
        self.detail_page_service = DetailPageService()

    @cache.cached(timeout=5000, key_prefix=detail_info_cache)
    def get(self):
        try:
            company_id = DetailInfoModel(**request.args.to_dict()).company_id
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.detail_page_service.detail_info(company_id)
        except Exception as e:
            return ResponseHandler(HTTPStatus.INTERNAL_SERVER_ERROR).response()

        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"


class DetailChartView(Resource):
    def __init__(self):
        self.detail_page_service = DetailPageService()

    @cache.cached(timeout=500, key_prefix=detail_chart_cache)
    def get(self):
        try:
            detail_chart = DetailChartModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.detail_page_service.detail_chart_graph(detail_chart.company_id, detail_chart.now)
        except Exception as e:
            return ResponseHandler(HTTPStatus.INTERNAL_SERVER_ERROR).response()

        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"
