from pydantic import BaseModel, validator, PositiveInt, ValidationError

class PageModel(BaseModel):
    start_page: int = 0
    per_page: PositiveInt = 30


class NowModel(BaseModel):
    now: str
