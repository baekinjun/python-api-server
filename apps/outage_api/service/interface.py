from abc import ABCMeta, abstractmethod
from apps.outage_api.repository import OutagePageDao, AfterDao


class OutageServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.outage_page_dao = OutagePageDao()


class OutageAfterServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.after_dao = AfterDao()

    @abstractmethod
    def up_view_cnt(self, req):
        pass
