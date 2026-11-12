from src.events.graph_events import NodeStatusEvent


class SupplierFailureEvent(NodeStatusEvent):
    def __init__(self, supplier_name):
        super().__init__("Lieferantenausfall", supplier_name, 1.0)
