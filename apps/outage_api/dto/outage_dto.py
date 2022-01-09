from pydantic import BaseModel, validator, ValidationError, constr
from typing import Optional
from core.common.common_validate import *


class MonthModel(BaseModel):
    now: str


class OutageListModel(BaseModel):
    company_id: Optional[int] = None
    period: str
    start_page: int = 0
    per_page: int = 30

    _page_valid = validator('start_page', 'per_page', allow_reuse=True)(must_up_zero)


class OutageSearchListModel(BaseModel):
    period: str = None
    search_keyword: constr(max_length=60)
    start_page: int = 0
    per_page: int = 30

    _page_valid = validator('start_page', 'per_page', allow_reuse=True)(must_up_zero)


class DetailOutageModel(BaseModel):
    company_id: int
    error_time: str

    _company_valid = validator('company_id', allow_reuse=True)(must_up_zero)
