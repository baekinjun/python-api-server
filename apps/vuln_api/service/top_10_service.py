from datetime import datetime
from .interface import VulnServiceInterface


class Top10VulnService(VulnServiceInterface):

    def top_10_outage(self, now: str) -> dict:
        nowt = datetime.strptime(now[0:10], '%Y-%m-%d')
        rs = self.vuln_dao.outage_top_10(nowt)
        return rs
