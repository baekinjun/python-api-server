# 외부 라이브러리
from flask_restful import Resource
from flask import request
from http import HTTPStatus

# 커스텀 코드
from apps.admin_api.service import AdminRegistrationService
from core.handler import ResponseHandler
from apps.admin_api.dto import *


class RegistartionView(Resource):
    def __init__(self):
        self.admin_page_service = AdminRegistrationService()

    def get(self):
        try:
            company_id = CompanyModel(**request.args.to_dict()).company_id
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        res = self.admin_page_service.get_registration(company_id)
        return ResponseHandler(HTTPStatus.OK).payload(res)

    def post(self):
        try:
            registration = PRegistrationModel(**request.form.to_dict())
            file = request.files['logo']
            FileModel(**{'file': file.filename})
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        file_name = self.admin_page_service.file_upload_to_azure(file)
        res = self.admin_page_service.add_registration(file_name, **registration.dict())
        return ResponseHandler(HTTPStatus.CREATED).response()


class URegistartionView(Resource):
    def __init__(self):
        self.admin_page_service = AdminRegistrationService()

    def post(self):
        try:
            company_id = CompanyModel(**request.form.to_dict()).company_id
            registration = PRegistrationModel(**request.form.to_dict())
            file = request.files['logo']
            FileModel(**{'file': file.filename})
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())

        file_name = self.admin_page_service.file_upload_to_azure(file)
        res = self.admin_page_service.update_registration(file_name, company_id, **registration.dict())
        if res == 404:
            return ResponseHandler(HTTPStatus.NOT_FOUND).response()
        elif res == 500:
            return ResponseHandler(HTTPStatus.INTERNAL_SERVER_ERROR).response()
        else:
            return ResponseHandler(HTTPStatus.CREATED).response()


class DRegistartionView(Resource):
    def __init__(self):
        self.admin_page_service = AdminRegistrationService()

    def post(self):
        try:
            company_id = CompanyModel(**request.form.to_dict()).company_id
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.PRECONDITION_REQUIRED).validator_response(v.json())
        res = self.admin_page_service.delete_registration(company_id)
        if res == 404:
            return ResponseHandler(HTTPStatus.NOT_FOUND).response()
        else:
            return ResponseHandler(HTTPStatus.CREATED).response()
