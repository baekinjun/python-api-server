from .interface import StaticsInterFace


class CveStatics(StaticsInterFace):
    def result(self):
        if self._data != None:
            rs = {'labels': list(map(lambda label: label['cve_id'], self._data)),
                  'count': list(map(lambda count: count['count'], self._data))}
            return rs
        else:
            return None


class ServerStatics(StaticsInterFace):
    def result(self):
        if self._data != None:
            rs = {'labels': list(map(lambda label: label['app_name'], self._data)),
                  'count': list(map(lambda count: count['count'], self._data))}
            return rs
        else:
            return None
