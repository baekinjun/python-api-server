from abc import ABCMeta, abstractmethod
from apps.main_page_api.repository import MainPageDao, AfterDao
from ..common_utils import MainUtils


class MainServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.main_page_dao = MainPageDao()
        self.main_utils = MainUtils(self.main_page_dao)


class MainAfterServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.after_dao = AfterDao()

    @abstractmethod
    def collect_keyword(self, req) -> None:
        pass
