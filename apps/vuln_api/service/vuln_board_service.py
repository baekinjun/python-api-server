from datetime import datetime
from .interface import VulnServiceInterface


class VulnBoardService(VulnServiceInterface):

    def vuln(self, now: str) -> dict:
        rs = {'info': self.vuln_board(now), 'total_count': self.vuln_count()}
        return rs

    def vuln_board(self, now: str) -> dict:
        nowt = datetime.strptime(now[0:10], '%Y-%m-%d')

        rs = self.vuln_dao.vuln_board(nowt)
        return rs

    def vuln_count(self) -> int:
        rs = self.vuln_dao.vuln_board_count()['count']
        return rs
