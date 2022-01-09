from abc import ABCMeta
from apps.admin_api.repository import AdminPageDao


class AdminServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.admin_page_dao = AdminPageDao()
