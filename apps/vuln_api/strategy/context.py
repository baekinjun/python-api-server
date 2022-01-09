from abc import ABCMeta


class StaticsStrategy:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._static_strategy = None

    def result(self):
        return self._static_strategy.result()

    def set_statics_strategy(self, static_class: object) -> object:
        self._static_strategy = static_class
