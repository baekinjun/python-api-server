from apps.middleware import RepositoryInterface
from datetime import datetime


class MainPageDao(RepositoryInterface):

    def keyword_category_search(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT distinct a.product_id , a.product_name,a.logo FROM product AS a 
                left JOIN product_description as b ON a.product_id = b.product_id
                left JOIN product_address as c on a.product_id = c.product_id 
                WHERE ((b.text LIKE %s) or (c.asn_name LIKE %s) or a.product_name LIKE %s) 
                and a.category = %s order by a.reg_dtime DESC limit %s,%s;""",
            args
        )

    def keyword_category_search_count(self, args: tuple) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(distinct a.product_id)as count FROM product AS a 
                left JOIN product_description as b ON a.product_id = b.product_id
                left JOIN product_address as c on a.product_id = c.product_id 
                WHERE ((b.text LIKE %s) or (c.asn_name LIKE %s) or a.product_name LIKE %s) 
                and a.category = %s """,
            args
        )

    def keyword_search(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT distinct a.product_id , a.product_name,a.logo FROM product AS a 
                left JOIN product_description as b ON a.product_id = b.product_id
                left JOIN product_address as c on a.product_id = c.product_id 
                WHERE (b.text LIKE %s) or (c.asn_name LIKE %s) or a.product_name LIKE %s
                order by a.reg_dtime DESC limit %s,%s;""",
            args
        )

    def keyword_search_count(self, args: tuple) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT  COUNT(distinct a.product_id ) as count FROM product AS a 
            left JOIN product_description as b ON a.product_id = b.product_id
            left JOIN product_address as c on a.product_id = c.product_id 
            WHERE (b.text LIKE %s) or (c.asn_name LIKE %s) or a.product_name LIKE %s;""",
            args
        )

    def category_search(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT product_id,product_name,logo 
            FROM product WHERE category = %s 
            ORDER BY reg_dtime DESC limit %s,%s""",
            args
        )

    def category_search_count(self, args: str) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) FROM product WHERE category = %s""",
            args
        )

    def total_search(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT a.product_id,a.product_name,a.logo FROM product as a
            join product_view as b on a.product_id=b.product_id ORDER BY b.view_count 
            DESC limit %s,%s;""",
            args
        )

    def total_search_count(self) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) FROM product"""
        )

    def total_pid(self) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT product_id FROM product;"""
        )

    def chart_graph(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT response_time,request_dtime FROM heartbeat 
            WHERE product_id = %s and request_dtime >= %s and request_dtime <= now()""",
            args
        )

    def category_list(self) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT category FROM product group by category;"""
        )

    def country_statics(self) -> dict:
        return self.conn_s.b_fetchall(
            """select A.org_country_code,count(A.org_country_code) as count
                from (SELECT distinct(product_id),org_country_code from product_address) A
                group by A.org_country_code
                order by count desc;"""
        )

    def country_search(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """select distinct(a.product_id) , a.product_name ,a.logo ,b.org_country_code from product as a
            join product_address as b on a.product_id = b.product_id where b.org_country_code = %s
            order by a.reg_dtime DESC limit %s,%s;""",
            args
        )

    def country_search_count(self, args: dict) -> dict:
        return self.conn_s.b_fetchone(
            """select count(distinct(a.product_id)) as count from product as a
                join product_address as b on a.product_id = b.product_id 
                where b.org_country_code = %s;""",
            args
        )

    def asn_statics(self) -> dict:
        return self.conn_s.b_fetchall(
            """select A.asn_name, count(A.asn_name) as count
                from (SELECT distinct product_id, asn_name from product_address) A
                group by A.asn_name
                order by count desc;"""
        )

    def asn_search(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """select  distinct(a.product_id) , a.product_name ,a.logo from product as a
            join product_address as b on a.product_id = b.product_id where asn_name=%s
            order by a.reg_dtime DESC limit %s,%s;""",
            args
        )

    def asn_search_count(self, args: str) -> dict:
        return self.conn_s.b_fetchone(
            """select  count(distinct(a.product_id)) as count  from product as a
                join product_address as b on a.product_id = b.product_id where asn_name=%s;""",
            args
        )

    def popular_keyword(self, args: datetime) -> dict:
        return self.conn_s.b_fetchall(
            """call sp_search_rank(%s)""",
            args
        )

    def percentile(self, args: int) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT b.response_time
                FROM (
                    SELECT response_time
                    FROM heartbeat
                    WHERE product_id = %s
                    AND request_dtime < DATE_ADD(CURDATE(), INTERVAL -1 DAY)
                    ORDER BY request_dtime DESC
                    LIMIT 864
                ) AS b
                ORDER BY b.response_time limit 777, 1;
                """, args
        )

    def recent_asn_outage(self, args) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT COUNT(b.asn_name) as count , b.asn_name FROM heartbeat_history as a 
                join product_address as b on a.product_id = b.product_id
                where a.reg_dtime between %s and now()
                GROUP BY b.asn_name order by count desc
                LIMIT 10;""", args
        )

    def recent_server_outage(self, args) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT substring_index(b.product_name,':',-1) as product_name ,count(a.product_id) as count 
            FROM heartbeat_history as a 
            join product as b on a.product_id = b.product_id
            where a.request_dtime between %s and now()
            group by a.product_id order by count desc
            LIMIT 10;""", args
        )

    def recent_outage_info(self) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT distinct(a.product_id),c.product_name,a.request_dtime,b.asn_name , c.logo FROM heartbeat_history as a 
                join (SELECT product_id,group_concat(distinct(asn_name) separator ' @@') as asn_name from product_address group by product_id) as b 
                on a.product_id = b.product_id
                join product as c on a.product_id = c.product_id
                order by a.request_dtime desc LIMIT 4;"""
        )

    def recent_outage_chart(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT response_time,request_dtime FROM heartbeat
             WHERE product_id = %s and request_dtime >= %s and request_dtime <= %s""",
            args
        )
