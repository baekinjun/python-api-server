from abc import ABCMeta
from core.db import Procedure
from flask import request
from core.db import DB


class RepositoryInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        GEO_LOCATION = request.headers.get('X-Client-Geo-Location')
        if GEO_LOCATION == None:
            GEO_LOCATION = 'all'
        self.conn_s = Procedure(DB[GEO_LOCATION])
