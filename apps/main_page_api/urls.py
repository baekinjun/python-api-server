from apps.main_page_api.controller import *

url_patterns = [
    (MainChartView, '/chart'),
    (MainChartCountView, '/chart-count'),
    (CategoryView, '/category-list'),
    (PidToalView, '/total-url'),
    (CountryAsnCountView, '/statics/count'),
    (CountryStatisticsView, '/statics/country'),
    (CountryStatisticsSearchView, '/statics/country-search'),
    (AsnStatisticsView, '/statics/asn'),
    (RecentAsnOutageView, '/statics/asn-outage'),
    (RecentServerOutageView, '/statics/site-outage'),
    (RecentOutageInfoChartView, '/statics/outage-info'),
    (AsnStatisticsSearchView, '/statics/asn-search'),
    (PopularKeywordView, '/popular-keyword')

]
