from datetime import datetime, timedelta
from .interface import MainServiceInterface


class MainRecentOutageService(MainServiceInterface):

    def search_date_type(self, now: str, type: str) -> datetime:
        nowt = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        if type == 'day':
            search_date = nowt - timedelta(days=1)

        elif type == 'week':
            search_date_tmp = nowt - timedelta(days=7)
            search_date = datetime.strptime(str(search_date_tmp)[0:10], '%Y-%m-%d')

        else:
            search_date_tmp = nowt - timedelta(days=30)
            search_date = datetime.strptime(str(search_date_tmp)[0:10], '%Y-%m-%d')
        return search_date

    def recent_asn_outage(self, now: str, type: str) -> dict:
        find_date = self.search_date_type(now, type)
        res = self.main_page_dao.recent_asn_outage(find_date)
        return res

    def recent_server_outage(self, now: str, type: str) -> dict:
        find_date = self.search_date_type(now, type)
        res = self.main_page_dao.recent_server_outage(find_date)
        return res

    def recent_outage_chart(self, product_id, request_dtime):
        rs = {'count': None, 'labels': None}
        dtime = datetime.strptime(request_dtime, '%Y-%m-%d %H:%M:%S')

        start_dtime = dtime - timedelta(hours=3)
        end_dtime = dtime + timedelta(hours=3)

        tmp = self.main_page_dao.recent_outage_chart((product_id, start_dtime, end_dtime))
        if tmp:
            rs['count'] = list(map(lambda chart: chart['response_time'], tmp))
            rs['labels'] = list(map(lambda label: str(label['request_dtime']), tmp))
        return rs

    def recent_outage_info(self) -> dict:
        rs = self.main_page_dao.recent_outage_info()
        for data in rs:
            data['asn_name'] = data['asn_name'].split('@@')
            data['date'] = data['request_dtime'].split()[0]
            data['time'] = data['request_dtime'].split()[1]
            data['chart_data'] = self.recent_outage_chart(data['product_id'], data['request_dtime'])

            if data['chart_data']['count'] != None:
                data['score'] = self.main_utils.score(data['chart_data']['count'], data['product_id'])
            else:
                data['score'] = None
            data.pop('request_dtime')

        return rs
