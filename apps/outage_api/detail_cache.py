from flask import request


def outage_statcis(**kwargs):
    now = request.args.get('now')[0:15]
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([now,country])
