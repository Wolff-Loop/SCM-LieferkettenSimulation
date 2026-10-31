from .base_event import Event


class WarEvent(Event):

    def __init__(
        self,
        country: str,
        severity: float = 1.0
    ):

        self.country = country
        self.severity = severity

        self.active = False

    def apply(self):

        self.active = True

    def revert(self):

        self.active = False