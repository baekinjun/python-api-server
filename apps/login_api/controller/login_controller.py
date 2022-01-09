from flask_restful import Resource
from core.handler import ResponseHandler
from apps.login_api.service import LoginApiService
from flask import request
from ..dto import SignUpModel, ValidationError
from http import HTTPStatus


class SignUpView(Resource):
    def __init__(self):
        self.login_service = LoginApiService()

    def post(self):
        try:
            sign_up_info = SignUpModel(**request.form)
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.BAD_REQUEST).validator_response(v.json())

        res = self.login_service.sign_up(**sign_up_info.dict())

        return ResponseHandler(HTTPStatus.CREATED).response()


class LoginView(Resource):
    def __init__(self):
        self.login_service = LoginApiService()

    def post(self):
        try:
            sign_up_info = SignUpModel(**request.form)
        except ValidationError as v:
            return ResponseHandler(HTTPStatus.BAD_REQUEST).validator_response(v.json())

        res = self.login_service.sign_up(**sign_up_info.dict())

        return ResponseHandler(HTTPStatus.CREATED).response()
