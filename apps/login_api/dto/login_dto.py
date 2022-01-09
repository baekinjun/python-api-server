from pydantic import BaseModel, EmailStr, validator, root_validator, ValidationError
from enum import Enum
from apps.login_api.service import LoginApiService


class AccountTypeEnum(str, Enum):
    naver = 'naver'
    kakao = 'kakao'
    google = 'google'


class SignUpModel(BaseModel):
    customer_email: EmailStr
    uid: str
    account_type: AccountTypeEnum
    marketing: bool
    personal_info: bool

    @root_validator
    def duplication_check(cls, values):
        email, types = values.get('customer_email'), values.get('account_type')
        if LoginApiService().duplication_check(email, types):
            raise ValueError('중복된 아이디')
        return values


class LoginModel(BaseModel):
    customer_email: EmailStr
    password: str
    account_type: str

    @root_validator(pre=True)
    def get_or_404_email(cls, values):
        email, types = values.get('customer_email'), values.get('account_type')
        if LoginApiService().find_email_in_db(email, types):
            raise ('없는 아이디')
        return values


        
