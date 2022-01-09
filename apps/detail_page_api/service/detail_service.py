from datetime import datetime, timedelta
from .interface import DetailServiceInterface


class DetailPageService(DetailServiceInterface):
    def baseline(self, now: str, company_id: int) -> dict:
        yesterday = datetime.strptime(now[0:13], '%Y-%m-%d %H') - timedelta(days=1)
        rs = self.detail_page_dao.baseline(company_id)
        if rs:
            rs = rs[yesterday.hour:] + rs[0:yesterday.hour]

            res = {'labels': list(map(lambda label: int(label['per_request_time']), rs)),
                   'count': list(map(lambda data: int(data['per_response_time']), rs))}
        else:
            return None
        return res

    def detail_info(self, company_id) -> dict:
        res = {'information': self.company_info(company_id),
               'location_info': self.location_info(company_id),
               'recent_outage': self.recent_outage(company_id)}

        return res

    def company_info(self, company_id: int) -> dict:
        res = self.detail_page_dao.detail_chart_info(company_id)
        return res

    def location_info(self, company_id: int) -> dict:
        location = self.detail_page_dao.detail_chart_location(company_id)
        if location[0]['local_address'] == '':
            location = []
        return location

    def detail_chart_graph(self, company_id: int, now: str) -> dict:
        res = self.main_utils.chart_graph(company_id, now)
        return res

    def recent_outage(self, company_id: int) -> dict:
        rs = self.detail_page_dao.recent_outage(company_id)
        if rs != None:
            for tmp in rs:
                tmp['date'] = str(tmp['request_dtime']).split()[0]
                tmp['time'] = str(tmp['request_dtime']).split()[1]
                tmp.pop('request_dtime')
        return rs
