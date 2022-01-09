from flask import request


def admin_page_cache(**kwargs):
    search_keyword = request.args.get("search_keyword", "")
    country = request.headers.get('X-Client-Geo-Location')
    return '&'.join([country, search_keyword])
