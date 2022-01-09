def country_valid(name: str) -> str:
    if name not in ['ko', 'en', 'ja', 'ar', 'cn']:
        raise ValueError('country values must in [ko, en, ja, ar, cn]')
    return name


def must_up_zero(page: int) -> int:
    if page < 0:
        raise ValueError('value must up zero')
    return page




