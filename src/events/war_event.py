from .base_event import Event


class WarEvent(Event):

    def __init__(
        self,
        country: str,
        severity: float = 1.0
    ):
        self.country = country
        self.severity = severity

    def apply(self):

        print(
            f"War active in {self.country}"
        )

    def revert(self):

        print(
            f"War ended in {self.country}"
        )