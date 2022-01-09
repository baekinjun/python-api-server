from apps.vuln_api.controller import *

url_patterns = [
    (VulnBoardView, '/board'),
    (ServerStaticsView, '/statics/server'),
    (CveStaticsView, '/statics/cve'),
    (TodayOutageView, '/top-outage')
]
