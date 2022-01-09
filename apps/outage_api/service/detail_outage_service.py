from core.handler.response_handler import ResponseHandler
from datetime import datetime, timedelta
from .interface import OutageServiceInterface


class OutageDetailService(OutageServiceInterface):

    def detail_outage(self, **kwargs) -> dict:
        res = {'outage_news': None}
        try:
            res['outage_info'] = self.detail_outage_info(kwargs['error_time'], kwargs['company_id'])
            res['outage_news'] = self.detail_news(kwargs['error_time'], kwargs['company_id'])
            res['location_info'] = self.outage_page_dao.detail_chart_location(kwargs['company_id'])
        except Exception as e:
            raise ResponseHandler(500).response()
        return res

    def detail_outage_info(self, error_time: str, company_id: int) -> dict:
        error_timet = datetime.strptime(error_time, '%Y-%m-%d %H:%M:%S')
        outage_info_args = (company_id, error_timet)
        try:
            res = self.outage_page_dao.detail_outage_info(outage_info_args)
            request_dtime = str(res['request_dtime']).split()
        except Exception as e:
            raise ResponseHandler(400).response()

        res['time'] = request_dtime[1]
        res['date'] = request_dtime[0]
        res.pop('request_dtime')

        return res

    def detail_chart_array(self, error_time: str, company_id: int) -> dict:
        res = []

        error_timet = datetime.strptime(error_time[0:16], '%Y-%m-%d %H:%M')
        first_time = error_timet - timedelta(hours=12)
        end_time = error_timet + timedelta(hours=12)

        args = (company_id, first_time, end_time)
        chart_data_list = self.outage_page_dao.detail_outage_chart(args)

        if chart_data_list != ():
            res = {'count': list(map(lambda chart: chart['response_time'], chart_data_list)),
                   'labels': list(map(lambda label: str(label['request_dtime']), chart_data_list))}

        return res

    def detail_news(self, error_time: str, company_id: int) -> dict:
        error_timet = datetime.strptime(error_time, '%Y-%m-%d %H:%M:%S') - timedelta(hours=2)
        end_time = error_timet + timedelta(hours=5)

        args = (error_timet, end_time, company_id)

        res = self.outage_page_dao.outage_news(args)

        return res
