from abc import ABC, abstractmethod


class Event(ABC):

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def revert(self):
        pass