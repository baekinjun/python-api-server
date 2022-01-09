from apps.middleware import RepositoryInterface


class OutagePageDao(RepositoryInterface):
    def outage_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """call sp_heartbeat_history_select(%s,%s,%s,%s)""",
            args
        )

    def outage_list_name(self, args: int) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT product_name FROM product where product_id = %s;""",
            args
        )

    def outage_list_cnt(self, args: tuple) -> dict:
        return self.conn_s.b_fetchone(
            """call sp_heartbeat_history_cnt(%s,%s)""",
            args
        )

    def outage_period_keyword_search_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT a.product_id,b.product_name,a.request_server,a.status,a.status_description,a.request_dtime 
                FROM tingim.heartbeat_history as a
                join product as b on a.product_id=b.product_id
                where b.product_name LIKE %s and a.reg_dtime > %s and a.reg_dtime < %s
                order by a.reg_dtime desc LIMIT %s,%s;""", args
        )

    def outage_period_keyword_search_list_cnt(self, args: tuple) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) as count FROM tingim.heartbeat_history as a
                join product as b on a.product_id=b.product_id
                where b.product_name LIKE %s and a.reg_dtime > %s and a.reg_dtime < %s
                order by a.reg_dtime desc;""", args
        )

    def outage_keyword_search_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """call sp_heartbeat_history_search(%s,%s,%s);""",
            args
        )

    def outage_keyword_search_list_cnt(self, args: str) -> dict:
        return self.conn_s.b_fetchone(
            """call sp_heartbeat_history_search_cnt(%s);""",
            args
        )

    def detail_outage_info(self, args: tuple) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT a.product_name , a.logo ,a.url,b.request_dtime,b.status,b.request_server , b.status_description,b.screen_shot_url from product as a 
            join heartbeat_history as b on a.product_id = b.product_id 
            where a.product_id=%s and b.request_dtime=%s;""",
            args
        )

    def detail_chart_location(self, args: int) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT ip_address,latitude,longitude,local_address,org_country_code,asn_name 
            FROM product_address WHERE product_id=%s""",
            args
        )

    def detail_outage_chart(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT response_time,request_dtime FROM heartbeat
             WHERE product_id = %s and request_dtime >= %s and request_dtime <= %s""",
            args
        )

    def outage_news(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT product_id,title,url,summary,news_place,post_dtime 
            FROM news_headline 
            where post_dtime > %s and post_dtime < %s and product_id = %s;""",
            args
        )

    def outage_count(self, args: tuple) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT count(*) as count 
            FROM heartbeat_history 
            where reg_dtime>=%s and reg_dtime <%s;""",
            args
        )

    def outage_name(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT b.product_name ,count(b.product_name) as count FROM heartbeat_history as a 
            join product as b on a.product_id=b.product_id  where a.reg_dtime>= %s and a.reg_dtime < %s
            group by b.product_name;""",
            args
        )
