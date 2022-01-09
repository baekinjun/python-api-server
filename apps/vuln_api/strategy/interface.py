from abc import ABCMeta, abstractmethod


class StaticsInterFace:
    __metaclass__ = ABCMeta

    def __init__(self, data):
        self._data = data

    @abstractmethod
    def result(self):
        pass
