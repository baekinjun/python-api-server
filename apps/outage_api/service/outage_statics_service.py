from datetime import datetime, timedelta
from .interface import OutageServiceInterface


class OutageStaticsService(OutageServiceInterface):

    def outage_stat(self, now: str) -> dict:
        rs = {'product_name': [], 'count': [], 'labels': []}
        yesterday = datetime.strptime(now[0:13], '%Y-%m-%d %H') - timedelta(days=1)
        for h in range(24):
            start = yesterday + timedelta(hours=h)
            next = yesterday + timedelta(hours=h + 1)
            args = (start, next)

            rs['count'].append(self.outage_page_dao.outage_count(args)['count'])
            rs['product_name'].append(self.outage_page_dao.outage_name(args))
            rs['labels'].append(str(start.hour))

        return rs
