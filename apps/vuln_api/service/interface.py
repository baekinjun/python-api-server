from abc import ABCMeta
from apps.vuln_api.repository import VulnDao


class VulnServiceInterface:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.vuln_dao = VulnDao()
