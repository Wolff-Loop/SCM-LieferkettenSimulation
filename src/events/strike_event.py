from src.events.graph_events import NodeStatusEvent


class StrikeEvent(NodeStatusEvent):
    def __init__(self, target, severity=1.0):
        super().__init__("Streik", target, severity)
