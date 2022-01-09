from pydantic import BaseModel, ValidationError, PositiveInt


class DetailInfoModel(BaseModel):
    company_id: PositiveInt


class DetailChartModel(BaseModel):
    company_id: PositiveInt
    now: str


class BaseLineModel(BaseModel):
    now: str
    company_id: int
