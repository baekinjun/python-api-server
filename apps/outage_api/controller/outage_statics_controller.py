# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus
from flasgger import swag_from

# 커스텀 코드
from ..service import OutageStaticsService
from core.handler import ResponseHandler
from ..dto import *

# 서드파티
from apps.middleware import cache

# 캐시키 규칙
from ..detail_cache import outage_statcis


class OutageStaticsView(Resource):
    def __init__(self):
        self.outage_page_service = OutageStaticsService()

    @cache.cached(timeout=500, key_prefix=outage_statcis)
    def get(self):
        try:
            now = MonthModel(**request.args.to_dict()).now
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.outage_page_service.outage_stat(now)
        return ResponseHandler(HTTPStatus.OK).payload(res)
