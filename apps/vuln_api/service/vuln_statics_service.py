from datetime import datetime, timedelta
from apps.vuln_api.strategy import StaticsStrategy, ServerStatics, CveStatics
from .interface import VulnServiceInterface


class VulnStaticsService(VulnServiceInterface):
    def __init__(self):
        super().__init__()
        self.statics_stragey = StaticsStrategy()

    def server_statics(self, now: str) -> dict:
        nowt = datetime.strptime(now[0:10], '%Y-%m-%d')
        yesterday = nowt - timedelta(days=1)
        data = self.vuln_dao.server_statics((yesterday, nowt))

        self.statics_stragey.set_statics_strategy(ServerStatics(data))
        return self.statics_stragey.result()

    def cve_statics(self, now: str) -> dict:
        nowt = datetime.strptime(now[0:10], '%Y-%m-%d')
        yesterday = nowt - timedelta(days=1)
        data = self.vuln_dao.cve_statics((yesterday, nowt))

        self.statics_stragey.set_statics_strategy(CveStatics(data))
        return self.statics_stragey.result()
