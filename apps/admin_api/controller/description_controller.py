# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus

# 커스텀 코드
from apps.admin_api.service import AdminDescriptionService
from core.handler import ResponseHandler
from apps.admin_api.dto import *


class DescriptionView(Resource):
    def __init__(self):
        self.admin_page_service = AdminDescriptionService()

    def get(self):
        try:
            description = DescriptionModel(**request.args.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.admin_page_service.get_description(description.company_id)

        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        try:
            description = DescriptionModel(**request.form.to_dict())

        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.admin_page_service.add_description(description.company_id, description.description)
        return ResponseHandler(HTTPStatus.CREATED).response()


class UDescriptionView(Resource):
    def __init__(self):
        self.admin_page_service = AdminDescriptionService()

    def post(self):
        try:
            description = DescriptionModel(**request.form.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        res = self.admin_page_service.update_description(description.company_id, description.description)

        if res == 404:
            return ResponseHandler(HTTPStatus.NOT_FOUND).response()
        else:
            return ResponseHandler(HTTPStatus.CREATED).response()


class DDescriptionView(Resource):
    def __init__(self):
        self.admin_page_service = AdminDescriptionService()

    def post(self):
        try:
            description = DescriptionModel(**request.form.to_dict())
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        res = self.admin_page_service.delete_description(description.company_id)
        if res == 404:
            return ResponseHandler(HTTPStatus.NOT_FOUND).response()
        else:
            return ResponseHandler(HTTPStatus.CREATED).response()
