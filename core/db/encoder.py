from datetime import datetime, timedelta, date
import decimal


def _encoder(data: dict):
    for key, val in data.items():
        if isinstance(val, timedelta):
            data[key] = str(val)
        elif isinstance(val, datetime):
            data[key] = val.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(val, date):
            data[key] = val.strftime('%Y-%m-%d')
        elif isinstance(val, decimal.Decimal):
            data[key] = int(val)
    return data


def dict_encoder(func):
    def wrapper(*args, **kwargs):
        rv = func(*args, **kwargs)
        if isinstance(rv, list):
            return list(map(_encoder, rv))
        elif isinstance(rv, dict):
            return _encoder(rv)

    return wrapper
