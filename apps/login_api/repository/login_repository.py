from core.db import DB
from core.db import Procedure
from flask import request


class LoginApiDao:
    def __init__(self):
        GEO_LOCATION = request.headers.get('X-Client-Geo-Location')
        if GEO_LOCATION == None:
            GEO_LOCATION = 'all'
        self.conn_s = Procedure(DB[GEO_LOCATION])

    def check_email(self, args: tuple) -> dict:
        return self.conn_s.b_fetchone(
            """""", args
        )

    def sign_up(self, args):
        return self.conn_s.b_execute(
            """INSERT INTO user_info(customer_email,uid,account_type,marketing,personal_info) values (%s,%s,%s,%s,%s)""",
            args
        )
