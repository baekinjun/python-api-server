import unittest
from datetime import datetime ,timedelta
from dateutil.relativedelta import relativedelta
from pydantic import ValidationError
import json

import sys

sys.path.append('../..')
from core.db.dbutils import *
from core.handler.exceptions import *
from management import create_app
from models import MonthModel, DetailOutageModel


class ListUnitTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.db = Procedure(hq_db)

    def test_category(self):
        response = self.app.get('/api_v1/client/category_list')
        data = json.loads(response.get_data())
        sql = G_SQLS['bounce_query']['category_list']
        res = {'category_list': []}
        for cate in self.db.b_fetchall(sql, ()):
            res['category_list'].append(cate['category'])

        self.assertEqual(ResponseHandler(200).payload(res), data)

    def test_month(self):
        response = self.app.get('/api_v1/client/month_data?now=2021-03-11 00:00:00')
        data = json.loads(response.get_data())
        now_data = datetime.strptime('2021-03-11 00:00:00'[0:7], '%Y-%m')
        res = {'period': []}
        for mon in range(12):
            each_month = now_data - relativedelta(months=mon)
            res['period'].append('{}-{}'.format(each_month.year, each_month.month))
        self.assertEqual(ResponseHandler(200).payload(res), data)

    def test_wrong_month(self):
        response = self.app.get('/api_v1/client/month_data')
        data = json.loads(response.get_data())
        try:
            a = MonthModel(**{"": ""}).now
        except ValidationError as v:
            self.assertEqual(ResponseHandler(412).validator_response(v.json()), data)

    def test_no_endpoint(self):
        response = self.app.post('/api_v1/client/month_data?now=2021-03-11 00:00:00')
        data = json.loads(response.get_data())
        self.assertEqual("This endpoint does not exist. Please check!", data)
        response = self.app.post('/api_v1/client/category_list')
        data = json.loads(response.get_data())
        self.assertEqual("This endpoint does not exist. Please check!", data)


class DetailOutageUnitTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.conn_s = Procedure(hq_db)

    def test_detail_outage_info(self):
        response = self.app.get('/api_v1/client/detail_outage?company_id=81&error_time=2021-02-22 11:44:43')
        data = json.loads(response.get_data())['data']['outage_info']

        error_time = datetime.strptime('2021-02-22 11:44:43', '%Y-%m-%d %H:%M:%S')
        outage_info_sql = G_SQLS['bounce_query']['detail_outage_info']
        outage_info_args = (81, error_time)

        res = {'information': None, 'location_info': None}

        info = self.conn_s.b_fetchone(outage_info_sql, outage_info_args)
        request_dtime = str(info['request_dtime']).split()

        info['time'] = request_dtime[1]
        info['date'] = request_dtime[0]
        info.pop('request_dtime')

        detail_chart_location_sql = G_SQLS['bounce_query']['detail_chart_location']
        location_args = (81)
        location = self.conn_s.b_fetchall(detail_chart_location_sql, location_args)

        if location[0]['local_address'] == '':
            location = []

        res['information'] = info
        res['location_info'] = location

        self.assertEqual(res, data)

    def test_detail_outage_chart(self):
        response = self.app.get('/api_v1/client/detail_outage?company_id=81&error_time=2021-02-22 11:44:43')
        data = json.loads(response.get_data())['data']['outage_chart']
        res = {'chart_data': None}
        error_time = datetime.strptime('2021-02-22 11:44:43'[0:16], '%Y-%m-%d %H:%M')
        first_time = error_time - timedelta(hours=12)
        end_time = error_time + timedelta(hours=12)

        sql = G_SQLS['bounce_query']['detail_outage_chart']
        args = (81, first_time, end_time)
        chart_data_list = self.conn_s.b_fetchall(sql, args)
        chart, labels = [], []
        if chart_data_list != ():
            for chart_data in chart_data_list:
                chart.append(chart_data['response_time'])
                labels.append(str(chart_data['request_dtime']))
                res['chart_data'] = {'count': chart, 'labels': labels}
        self.assertEqual(res, data)

    def test_wrong_month(self):
        response = self.app.get('/api_v1/client/detail_outage')
        data = json.loads(response.get_data())
        try:
            a = DetailOutageModel(**{"": ""})
        except ValidationError as v:
            self.assertEqual(ResponseHandler(412).validator_response(v.json()), data)

    def test_no_endpoint(self):
        response = self.app.post('/api_v1/client/detail_outage')
        data = json.loads(response.get_data())
        self.assertEqual("This endpoint does not exist. Please check!", data)







if __name__ == "__main__":
    unittest.main()
