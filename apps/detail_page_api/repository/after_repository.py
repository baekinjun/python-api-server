from apps.middleware import RepositoryInterface


class AfterDao(RepositoryInterface):

    def up_view_cnt(self, args) -> None:
        return self.conn_s.b_execute(
            """call sp_product_view_increment(%s)""", args)
