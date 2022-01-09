from apps.middleware import RepositoryInterface


class DetailPageDao(RepositoryInterface):

    def baseline(self, args: int) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT product_id,per_request_time,per_response_time
             FROM stat where product_id=%s order by per_request_time """,
            args
        )

    def detail_chart_info(self, args: int) -> dict:
        return self.conn_s.b_fetchone(
            """select product_id,product_name ,category ,logo,url  FROM product 
            where product_id = %s;""",
            args
        )

    def detail_chart_location(self, args: int) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT ip_address,latitude,longitude,local_address,org_country_code,asn_name 
            FROM product_address WHERE product_id=%s order by reg_dtime""",
            args
        )

    def recent_outage(self, args: int) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT a.product_id , a.request_dtime ,b.product_name from heartbeat_history as a 
            join product as b on a.product_id=b.product_id where a.product_id=%s order by request_dtime desc LIMIT 0,5;""",
            args
        )
