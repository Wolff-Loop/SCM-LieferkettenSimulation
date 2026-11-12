from abc import ABC, abstractmethod


class Event(ABC):
    def __init__(self, name, target=None, severity=1.0):
        self.name = name
        self.target = target
        self.severity = severity
        self.active = False

    @abstractmethod
    def apply(self, application):
        pass

    @abstractmethod
    def revert(self, application):
        pass
