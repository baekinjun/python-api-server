from flask import request


def detail_info_cache(**kwargs):
    company_id = request.args.get('company_id')
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join(['detail_info', country, company_id])


def detail_chart_cache(**kwargs):
    now = request.args.get('now')[0:15]
    company_id = request.args.get('company_id')
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, now, company_id])
