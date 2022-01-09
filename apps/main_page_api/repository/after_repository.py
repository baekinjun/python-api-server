from apps.middleware import RepositoryInterface


class AfterDao(RepositoryInterface):
    def collect_keyword(self, args: tuple) -> None:
        return self.conn_s.b_execute(
            """INSERT INTO search(category ,keyword) values (%s,%s)""", args
        )
