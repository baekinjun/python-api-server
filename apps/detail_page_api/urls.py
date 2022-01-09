from apps.detail_page_api.controller import *

url_patterns = [
    (DetailChartView, '/chart'),
    (DetailInfoView, '/info'),
    (BaseLineView, '/base-line'),
]
