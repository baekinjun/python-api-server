# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from flasgger import swag_from

# 커스텀 코드
from core.handler import ResponseHandler
from apps.main_page_api.service import MainStaticsService
from apps.main_page_api.dto import *

# 서드파티
from apps.middleware import cache

# 캐시키 규칙
from apps.main_page_api.main_cache import (country_cache_key, asn_cache_key, get_country_cache_key, get_asn_cache_key,
                                           country_asn_count_key)


class CountryStatisticsView(Resource):
    def __init__(self):
        self.main_page_service = MainStaticsService()

    @cache.cached(timeout=200, key_prefix=get_country_cache_key)
    def get(self):
        res = self.main_page_service.country_statistics()
        return ResponseHandler(HTTPStatus.OK).payload(res)


class CountryStatisticsSearchView(Resource):
    def __init__(self):
        self.main_page_service = MainStaticsService()

    @cache.cached(timeout=500, key_prefix=country_cache_key)
    def get(self):
        try:
            c_stat = CountryStatisticsModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.main_page_service.country_info(**c_stat.dict())
        except Exception as e:
            return ResponseHandler(HTTPStatus.BAD_REQUEST).response()

        return ResponseHandler(HTTPStatus.OK).payload(res)


class AsnStatisticsView(Resource):
    def __init__(self):
        self.main_page_service = MainStaticsService()

    @cache.cached(timeout=200, key_prefix=get_asn_cache_key)
    def get(self):
        res = self.main_page_service.asn_statistics()
        return ResponseHandler(HTTPStatus.OK).payload(res)


class AsnStatisticsSearchView(Resource):
    def __init__(self):
        self.main_page_service = MainStaticsService()

    @cache.cached(timeout=500, key_prefix=asn_cache_key)
    def get(self):
        try:
            a_stat = AsnStatisticsModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        try:
            res = self.main_page_service.asn_info(**a_stat.dict())
        except Exception as e:
            return ResponseHandler(HTTPStatus.BAD_REQUEST).response()

        return ResponseHandler(HTTPStatus.OK).payload(res)


class CountryAsnCountView(Resource):
    def __init__(self):
        self.main_page_service = MainStaticsService()

    @cache.cached(timeout=6000, key_prefix=country_asn_count_key)
    def get(self):
        try:
            country_asn = CountryAsnCountModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.main_page_service.country_asn_count(country_asn.country_code, country_asn.asn_name)
        return ResponseHandler(HTTPStatus.OK).payload(res)
