from core.config import G_DATABASE
import pymysql, urllib3
from dbutils.pooled_db import PooledDB

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DB = dict()
c_list = ['all', 'ja']
for country in c_list:
    DB[country] = PooledDB(
        ping=7,
        creator=pymysql,
        cursorclass=pymysql.cursors.DictCursor,
        mincached=2,
        blocking=True,
        charset='utf8mb4',
        use_unicode=True,
        autocommit=True,
        maxconnections=G_DATABASE['maxconnections'],
        port=G_DATABASE['port'],
        host=G_DATABASE['host'],
        user=G_DATABASE['user'],
        password=G_DATABASE['password'],
        db=G_DATABASE['schema'][country]
    )
