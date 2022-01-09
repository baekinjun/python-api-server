from datetime import datetime, timedelta


class MainUtils:
    def __init__(self, dao):
        self.dao = dao

    def score(self, chart_data: dict, product_id: int) -> str:
        percentile = self.dao.percentile(product_id)
        if percentile == None:
            return 'dangerous'
        else:
            percentile = percentile['response_time']

        three_our = int(len(chart_data) * 0.875)
        three_data = chart_data[three_our:]

        critical = len(list(filter(lambda x: x >= percentile * 3, three_data)))
        score_cnt = len(list(filter(lambda x: x >= percentile, three_data)))

        if critical:
            return 'critical'

        if score_cnt > int(len(three_data) * 0.6):
            return "critical"
        elif score_cnt > int(len(three_data) * 0.3):
            return "dangerous"
        else:
            return "safe"

    def chart_graph(self, p_id: int, now: datetime) -> dict:
        res = {'count': None, 'labels': None}

        nowt = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        start_dtime = datetime.strptime(str(nowt - timedelta(days=1))[0:16], '%Y-%m-%d %H:%M')

        args = (p_id, start_dtime)

        chart_data = self.dao.chart_graph(args)
        if chart_data != None:
            res['count'] = list(map(lambda chart: chart['response_time'], chart_data))
            res['labels'] = list(map(lambda label: str(label['request_dtime']), chart_data))
        return res

    def make_list_graph(self, res, now):
        if res != None:
            for data in res:
                data['chart_data'] = self.chart_graph(data['product_id'], now)
                print(self.chart_graph(data['product_id'], now))
                if data['chart_data']['count'] != None:
                    data['score'] = self.score(data['chart_data']['count'], data['product_id'])
                else:
                    data['score'] = None
        return res
