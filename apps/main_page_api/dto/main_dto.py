from pydantic import BaseModel, validator, PositiveInt, ValidationError, root_validator, constr
from enum import Enum

from typing import Optional
from core.common.common_validate import *


class MainChartModel(BaseModel):
    start_page: Optional[int] = 0
    per_page: Optional[int] = 20
    category: Optional[str] = None
    search_keyword: Optional[constr(max_length=60)] = None
    now: str
    _page_valid = validator('start_page', 'per_page', allow_reuse=True)(must_up_zero)


class MainChartCountModel(BaseModel):
    category: Optional[str] = None
    search_keyword: Optional[str] = None


class CountryStatisticsModel(BaseModel):
    now: str
    country_code: str
    start_page: int = 0
    per_page: PositiveInt = 30


class AsnStatisticsModel(BaseModel):
    now: str
    asn_name: str
    start_page: int = 0
    per_page: PositiveInt = 30


class CountryAsnCountModel(BaseModel):
    country_code: Optional[str] = None
    asn_name: Optional[str] = None

    @root_validator
    def check_one_value(cls, values):
        country_code, asn_name = values.get('country_code'), values.get('asn_name')
        if country_code == None and asn_name == None:
            raise ValueError('must contain one value')
        elif country_code and asn_name:
            raise ValueError("you should input one value")
        return values


class MonthModel(BaseModel):
    now: str


class DateTypeEnum(str, Enum):
    day = 'day'
    week = 'week'
    month = 'month'


class StaticsModel(BaseModel):
    date_type: DateTypeEnum
    now: str
