from abc import ABCMeta, abstractmethod
from apps.main_page_api.common_utils import MainUtils
from apps.main_page_api.repository import MainPageDao
from apps.detail_page_api.repository import DetailPageDao, AfterDao


class DetailServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.detail_page_dao = DetailPageDao()
        self.main_utils = MainUtils(MainPageDao())


class DetailAfterServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.after_dao = AfterDao()

    @abstractmethod
    def up_view_cnt(self, req) -> None:
        pass
