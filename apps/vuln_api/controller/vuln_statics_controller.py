from flask_restful import Resource
from core.handler import ResponseHandler
from apps.vuln_api.service import VulnStaticsService
from apps.vuln_api.dto import *
from flask import request
from http import HTTPStatus
from flasgger import swag_from


class ServerStaticsView(Resource):
    def __init__(self):
        self.vuln_service = VulnStaticsService()

    def get(self):
        try:
            now = NowModel(**request.args.to_dict()).now
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.vuln_service.server_statics(now)

        return ResponseHandler(HTTPStatus.OK).payload(res)


class CveStaticsView(Resource):
    def __init__(self):
        self.vuln_service = VulnStaticsService()

    def get(self):
        try:
            now = NowModel(**request.args.to_dict()).now
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.vuln_service.cve_statics(now)

        return ResponseHandler(HTTPStatus.OK).payload(res)
