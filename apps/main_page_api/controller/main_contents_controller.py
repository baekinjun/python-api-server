# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from flasgger import swag_from

# 커스텀 코드
from core.handler import ResponseHandler
from apps.main_page_api.service import MainContentsService
from apps.main_page_api.dto import *

# 서드파티
from apps.middleware import cache, compress

# 캐시키 규칙
from apps.main_page_api.main_cache import (main_chart_cache_key, pid_cache_key, main_chart_count_cache_key)


class MainChartView(Resource):
    def __init__(self):
        self.main_page_service = MainContentsService()

    @cache.cached(timeout=500, key_prefix=main_chart_cache_key)
    @compress.compressed()
    def get(self):
        try:
            main_chart = MainChartModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.main_page_service.type_search(**main_chart.dict())
            if res == None:
                return ResponseHandler(HTTPStatus.NO_CONTENT).response()
        except Exception as e:
            return ResponseHandler(HTTPStatus.BAD_REQUEST).response()

        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"


class MainChartCountView(Resource):
    def __init__(self):
        self.main_page_service = MainContentsService()

    @cache.cached(timeout=6000, key_prefix=main_chart_count_cache_key)
    def get(self):
        try:
            main_chart = MainChartCountModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.main_page_service.type_search_count(**main_chart.dict())
        except Exception as e:
            return ResponseHandler(HTTPStatus.BAD_REQUEST).response()

        return ResponseHandler(HTTPStatus.OK).payload(res)


class CategoryView(Resource):
    def __init__(self):
        self.main_page_service = MainContentsService()

    def get(self):
        cate_list = self.main_page_service.category_list()
        return ResponseHandler(HTTPStatus.OK).payload(cate_list)

    def post(self):
        return "This endpoint does not exist. Please check!"


class PidToalView(Resource):
    def __init__(self):
        self.main_page_service = MainContentsService()

    @cache.cached(timeout=1000, key_prefix=pid_cache_key)
    def get(self):
        res = self.main_page_service.total_pid()

        return ResponseHandler(HTTPStatus.OK).payload(res)


class PopularKeywordView(Resource):
    def __init__(self):
        self.main_page_service = MainContentsService()

    def get(self):
        try:
            now = MonthModel(**request.args.to_dict()).now
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.main_page_service.popular_keyword(now)

        return ResponseHandler(HTTPStatus.OK).payload(res)
