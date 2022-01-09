from flask import request


def main_chart_cache_key(**kwargs):
    now = request.args.get('now')[0:15]
    search_keyword = request.args.get("search_keyword", '')
    category = request.args.get('category', '')
    start_page = request.args.get('start_page', 0)
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, now, search_keyword, str(start_page), category])


def main_chart_count_cache_key(**kwargs):
    search_keyword = request.args.get("search_keyword", '')
    category = request.args.get('category', '')
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, search_keyword, category])


def get_country_cache_key(**kwargs):
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, 'country'])


def pid_cache_key(**kwargs):
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, 'pid'])


def get_asn_cache_key(**kwargs):
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, 'asn'])


def country_cache_key(**kwargs):
    now = request.args.get('now')[0:15]
    country_code = request.args.get('country_code')
    start_page = request.args.get('start_page', 0)
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, now, country_code, str(start_page)])


def asn_cache_key(**kwargs):
    now = request.args.get('now')[0:15]
    asn_name = request.args.get('asn_name')
    start_page = request.args.get('start_page', 0)
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, now, asn_name, str(start_page)])


def country_asn_count_key(**kwargs):
    asn_name = request.args.get('asn_name', '')
    country_code = request.args.get('country_code', '')
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, asn_name, country_code])
