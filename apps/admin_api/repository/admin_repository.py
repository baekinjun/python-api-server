from apps.middleware import RepositoryInterface


class AdminPageDao(RepositoryInterface):

    def homepage_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT * FROM schedule WHERE type = 'homepage' ORDER BY reg_dtime DESC LIMIT %s,%s"""
            , args
        )

    def homepage_total_count(self) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) as  total_count FROM schedule WHERE type = 'homepage'"""
        )

    def homepage_search_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT * FROM schedule WHERE type = 'homepage' and name LIKE %s ORDER BY reg_dtime DESC LIMIT %s,%s""",
            args
        )

    def homepage_search_list_cnt(self, args: str) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) as  total_count  FROM schedule WHERE type = 'homepage' and name LIKE %s """,
            args
        )

    def api_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT * FROM schedule WHERE type = 'api' ORDER BY reg_dtime DESC LIMIT %s,%s """,
            args
        )

    def api_total_count(self) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) as total_count FROM schedule WHERE type = 'api'"""
        )

    def api_search_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT * FROM schedule WHERE type = 'api' and name LIKE %s ORDER BY reg_dtime DESC LIMIT %s,%s""",
            args
        )

    def api_search_list_cnt(self, args: str) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) as  total_count  FROM schedule WHERE type = 'api' and name LIKE %s """,
            args
        )

    def get_one_description(self, args: int) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT product_id,text FROM product_description WHERE product_id=%s""",
            args
        )

    def add_description(self, args: tuple) -> None:
        return self.conn_s.b_execute(
            """call sp_product_description_set(%s, %s);""",
            args
        )

    def update_description(self, args: tuple) -> None:
        return self.conn_s.b_execute(
            """UPDATE product_description SET text=%s where product_id = %s""",
            args
        )

    def delete_description(self, args: int) -> None:
        return self.conn_s.b_execute(
            """DELETE FROM product_description WHERE product_id = %s""",
            args
        )

    def one_product_set(self, args: int) -> dict:
        return self.conn_s.b_fetchone(
            """call sp_product_select(%s);""",
            args
        )

    def registration_set(self, args: list) -> dict:
        return self.conn_s.b_execute(
            """call sp_registration(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
            args
        )

    def get_id(self, args: str) -> dict:
        return self.conn_s.b_execute(
            """SELECT product_id FROM product WHERE url=%s""",
            args
        )

    def product_address_add(self, args: tuple) -> None:
        return self.conn_s.b_execute(
            """call sp_product_address_add(%s,%s,%s,%s,%s,%s,%s)""",
            args
        )

    def update_registration_set(self, args: list) -> None:
        return self.conn_s.b_execute(
            """call sp_product_update(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
            args
        )

    def product_address_reset(self, args: int) -> None:
        return self.conn_s.b_execute(
            """call sp_product_address_reset(%s)""",
            args
        )

    def delete_registration_set(self, args: int) -> None:
        return self.conn_s.b_execute(
            """call sp_product_del(%s);""",
            args
        )

    def search_keyword_list(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT * FROM search order by reg_dtime desc LIMIT %s,%s""",
            args
        )

    def search_keyword_list_cnt(self) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT COUNT(*) as count FROM search;"""
        )

    def news_data(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT a.ROWID,b.product_name,a.news_place,a.title,a.url,a.summary,a.post_dtime
                from news_headline as a join product as b on a.product_id = b.product_id 
                order by a.post_dtime desc LIMIT %s,%s;""",
            args
        )

    def news_data_cnt(self) -> dict:
        return self.conn_s.b_fetchone(
            """select COUNT(*) as count FROM news_headline"""
        )

    def news_search_data(self, args: tuple) -> dict:
        return self.conn_s.b_fetchall(
            """SELECT a.ROWID,b.product_name,a.news_place,a.title,a.url,a.summary,a.post_dtime
                from news_headline as a join product as b on a.product_id = b.product_id 
                where b.product_name LIKE %s
                order by a.post_dtime desc LIMIT %s,%s;""",
            args
        )

    def news_search_count(self, args: str) -> dict:
        return self.conn_s.b_fetchone(
            """SELECT count(a.ROWID) as count
                from news_headline as a join product as b on a.product_id = b.product_id 
                where b.product_name LIKE %s;""",
            args
        )

    def delete_news_data(self, args: int) -> dict:
        return self.conn_s.b_execute(
            """DELETE FROM news_headline where ROWID=%s""",
            args
        )
