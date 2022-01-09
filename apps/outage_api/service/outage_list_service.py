from datetime import datetime
from .interface import OutageServiceInterface
from dateutil.relativedelta import relativedelta


class OutageListService(OutageServiceInterface):

    def outage_list(self, period: str, start_page: int, per_page: int, company_id: int) -> dict:
        res = dict()
        first_period = datetime.strptime(period[0:7], '%Y-%m')
        args = (company_id, str(first_period)[0:10], (start_page * per_page), per_page)
        outage_info = self.outage_page_dao.outage_list(args)
        if outage_info == None:
            return None

        for info in outage_info:
            info['date'] = str(info['request_dtime']).split()[0]
            info['time'] = str(info['request_dtime']).split()[1]
            info.pop('request_dtime')

        total_count_args = (company_id, first_period)

        total_count = self.outage_page_dao.outage_list_cnt(total_count_args)

        res['outage_history'] = outage_info
        res['total_count'] = total_count['count(*)']

        if company_id != None:
            res['product_name'] = self.outage_page_dao.outage_list_name(company_id)['product_name']

        return res

    def outage_search(self, period: str, keyword: str, start_page: int, per_page: int) -> dict:
        if period == None:
            res = self.outage_keyword_search_list(keyword, start_page, per_page)
        else:
            res = self.outage_keyword_period_search_list(period, keyword, start_page, per_page)
        return res

    def outage_keyword_period_search_list(self, period: str, keyword: str, start_page: int, per_page: int) -> dict:
        res = {'outage_history': None}

        first_period = datetime.strptime(period[0:7], '%Y-%m')
        last_period = first_period + relativedelta(months=1)

        args = ('%%' + keyword + '%%', first_period, last_period, (start_page * per_page), per_page)

        search_outage_info = self.outage_page_dao.outage_period_keyword_search_list(args)
        search_outage_cnt = self.outage_page_dao.outage_period_keyword_search_list_cnt(
            ('%%' + keyword + '%%', first_period, last_period))

        for info in search_outage_info:
            info['date'] = str(info['request_dtime']).split()[0]
            info['time'] = str(info['request_dtime']).split()[1]
            info.pop('request_dtime')

        res['outage_history'] = search_outage_info
        res['total_count'] = search_outage_cnt['count']

        return res

    def outage_keyword_search_list(self, keyword: str, start_page: int, per_page: int) -> dict:
        res = {'outage_history': None, 'total_count': 0}
        args = (keyword, (start_page * per_page), per_page)

        search_outage_info = self.outage_page_dao.outage_keyword_search_list(args)
        search_outage_cnt = self.outage_page_dao.outage_keyword_search_list_cnt(keyword)
        if search_outage_info:
            for info in search_outage_info:
                info['date'] = str(info['request_dtime']).split()[0]
                info['time'] = str(info['request_dtime']).split()[1]
                info.pop('request_dtime')

            res['outage_history'] = search_outage_info
            res['total_count'] = search_outage_cnt['count(*)']

        return res

    def monthly_data(self, now: str) -> list:
        now_data = datetime.strptime(now[0:7], '%Y-%m')
        res = list(map(lambda mon=0: '{}-{}'.format((now_data - relativedelta(months=mon)).year,
                                                    (now_data - relativedelta(months=mon)).month),
                       range(12)))
        return res
