class Scenario:

    def __init__(
        self,
        name: str
    ):

        self.name = name

        self.events = []

    def add_event(
        self,
        event
    ):

        self.events.append(
            event
        )