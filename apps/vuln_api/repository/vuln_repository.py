from datetime import datetime
from apps.middleware import RepositoryInterface


class VulnDao(RepositoryInterface):
    def vuln_board(self, now: datetime) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT b.product_name,b.url,a.product_id,a.ip_address,a.open_port_no,a.cve_id,a.app_name,a.app_version,a.scan_dtime
                from stat_vulnerability as a 
                join product as b 
                on a.product_id = b.product_id  
                where a.reg_dtime >= %s 
                order by a.scan_dtime desc;""",
            (now)
        )

    def vuln_board_count(self) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) as count 
            from stat_vulnerability as a 
            join product as b on a.product_id = b.product_id;"""
        )

    def server_statics(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """select app_name,count(app_name) as count 
            from stat_vulnerability 
            where reg_dtime >=%s and reg_dtime < %s 
            group by app_name order by count desc;""",
            args
        )

    def cve_statics(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """select cve_id,count(cve_id) as count 
            from stat_vulnerability
             where reg_dtime >=%s and reg_dtime < %s
            group by cve_id order by count desc;""",
            args
        )

    def outage_top_10(self, now: datetime) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT b.product_name , count(b.product_name)as count 
            FROM heartbeat_history as a 
            join product as b on a.product_id=b.product_id 
            where a.reg_dtime > %s group by b.product_name 
            order by count desc limit 0,10;""",
            now
        )
