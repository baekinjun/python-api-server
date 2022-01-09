import psycopg2 as pg
from psycopg2 import pool
from config_chat import database_info, log
import json

pg_pool = pg.pool.SimpleConnectionPool(1, 10, host=database_info['host'], database=database_info['database'],
                                       user=database_info['user'], password=database_info['password'],
                                       port=database_info['port'])


def insert_pg(data):
    if (pg_pool == False):
        log.log_warning(400, "db connection error")
        raise ConnectionError("db connection error")

    data_set = {
        'name': data['nickname'],
        'msg': data['message'],
        'ip': data['client_ip'],
        'ts': data['real_time']
    }
    try:
        with pg_pool.getconn() as conn:
            conn.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

            with conn.cursor() as curs:
                curs.execute("NOTIFY api_{}, '{}';".format(data['room'], json.dumps(data_set, ensure_ascii=False)))

    except Exception as e:
        log.log_info(str(e))
    finally:
        if pg_pool:
            pg_pool.putconn(conn)
