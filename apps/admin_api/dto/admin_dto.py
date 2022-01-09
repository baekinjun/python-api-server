from pydantic import BaseModel, validator, PositiveInt, ValidationError
from typing import Optional
from core.common.common_validate import *


class PageListModel(BaseModel):
    start_page: int = 0
    per_page: int = 10
    search_keyword: Optional[str] = None

    _page_valid = validator('start_page', 'per_page', allow_reuse=True)(must_up_zero)


class DescriptionModel(BaseModel):
    company_id: int
    description: Optional[str] = ''
    product_name: Optional[str] = ''


class PRegistrationModel(BaseModel):
    company_name: str
    category: str
    product_name: str
    url: str
    status: str = '["200"]'
    time_interval: int = 10
    comment: str = None
    page_type: str = 'homepage'
    method: str = 'GET'
    params: str = '[]'
    header: str = '[]'


class CompanyModel(BaseModel):
    company_id: int

    _company_valid = validator('company_id', allow_reuse=True)(must_up_zero)


class RowidModel(BaseModel):
    rowid: PositiveInt



class FileModel(BaseModel):
    file: str
    @validator('file')
    def allow_file_extension(cls, file: str) -> str:
        file_extension = file.rsplit('.', 1)[1]
        if file_extension not in ['jpg', 'png', 'PNG', 'JPG']:
            raise ValueError('not allowed file extension')
        return file
