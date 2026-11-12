from src.events.graph_events import NodeStatusEvent


class WarEvent(NodeStatusEvent):
    def __init__(self, country, severity=1.0):
        super().__init__("Krieg", country, severity)
        self.country = country
