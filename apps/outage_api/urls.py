from .controller import *

url_patterns = [
    (OutageListView, '/history'),
    (DetailOutageInfoView, '/info'),
    (DetailOutageChartView, '/chart'),
    (OutageStaticsView, '/statics'),
    (MonthDataView, '/month-data'),
    (OutageSearchListView, '/search')
]
