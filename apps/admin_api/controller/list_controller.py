# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus

# 커스텀 코드
from apps.admin_api.service import AdminListService
from core.handler import ResponseHandler
from apps.admin_api.dto import *

# 서드파티
from apps.middleware import cache

# 캐시키 규칙
from apps.admin_api.admin_cache import admin_page_cache


class HomePageListView(Resource):
    def __init__(self):
        self.admin_page_service = AdminListService()

    @cache.cached(timeout=500, key_prefix=admin_page_cache)
    def get(self):
        try:
            page = PageListModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        res = self.admin_page_service.get_home_list(page.start_page, page.per_page, page.search_keyword)
        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"


class ApiListView(Resource):
    def __init__(self):
        self.admin_page_service = AdminListService()

    @cache.cached(timeout=500, key_prefix=admin_page_cache)
    def get(self):
        try:
            page = PageListModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.admin_page_service.get_api_list(page.start_page, page.per_page, page.search_keyword)
        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        return "This endpoint does not exist. Please check!"


class SearchKeywordListView(Resource):
    def __init__(self):
        self.admin_page_service = AdminListService()

    def get(self):
        try:
            page = PageListModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        res = self.admin_page_service.s_keyword_list(page.start_page, page.per_page)
        return ResponseHandler(HTTPStatus.OK).payload(res)


class NewsDataView(Resource):
    def __init__(self):
        self.admin_page_service = AdminListService()

    def get(self):
        try:
            page = PageListModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        res = self.admin_page_service.get_news_list(page.start_page, page.per_page, page.search_keyword)
        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        try:
            row_id = RowidModel(**request.form.to_dict()).rowid
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.admin_page_service.delete_news_list(row_id)

        return ResponseHandler(HTTPStatus.CREATED).response()
