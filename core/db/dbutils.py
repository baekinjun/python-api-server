import pymysql
from core.handler.exceptions import ExecuteError
from .encoder import dict_encoder
from core.config import G_LOG


class Procedure:
    def __init__(self, db):
        self.db = db

    @dict_encoder
    def b_fetchone(self, sql, args=()):
        conn = self.db.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, args)
            rs = cursor.fetchone()
        except Exception as e:
            G_LOG.log_info(str(e))
            return ExecuteError(sql, e).to_dict()
        finally:
            cursor.close()
            conn.close()

        return rs

    @dict_encoder
    def b_fetchall(self, sql, args=()):
        conn = self.db.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, args)
            rs = cursor.fetchall()
        except Exception as e:
            return ExecuteError(sql, e).to_dict()
        finally:
            cursor.close()
            conn.close()

        return rs

    @dict_encoder
    def b_execute(self, sql, args=()):
        conn = self.db.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, args)
            cursor.execute("SELECT @o_out_code;")
            row = cursor.fetchone()
            rs = row['@o_out_code']
        except Exception as e:
            G_LOG.log_info(str(e))
            return ExecuteError(sql, e).to_dict()
        finally:
            conn.commit()
            cursor.close()
            conn.close()
        return rs

    @dict_encoder
    def b_execute_many(self, sql, args=()):
        conn = self.db.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.executemany(sql, args)
            cursor.execute("SELECT @o_out_code;")
            rs = cursor.fetchone()
        except Exception as e:
            G_LOG.log_info(str(e))
            return ExecuteError(sql, e).to_dict()
        finally:
            conn.commit()
            cursor.close()
            conn.close()
        return rs
