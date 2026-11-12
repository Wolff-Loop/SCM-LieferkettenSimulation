from src.events.base_event import Event


class NodeStatusEvent(Event):
    def __init__(self, name, target, severity=1.0):
        super().__init__(name, target, severity)
        self.changed_nodes = []

    def apply(self, application):
        if self.active:
            return
        node_ids = application.node_ids_for_name_or_country(self.target)
        for node_id in node_ids:
            old_status = application.graph.nodes[node_id].get("status", "ACTIVE")
            self.changed_nodes.append((node_id, old_status))
            application.graph.nodes[node_id]["status"] = "INACTIVE"
        self.active = True

    def revert(self, application):
        for node_id, old_status in self.changed_nodes:
            if node_id in application.graph:
                application.graph.nodes[node_id]["status"] = old_status
        self.changed_nodes.clear()
        self.active = False


class EdgeStatusEvent(Event):
    def __init__(self, name, source, target):
        super().__init__(name, f"{source}->{target}", 1.0)
        self.source = source
        self.edge_target = target
        self.old_status = None

    def apply(self, application):
        if application.graph.has_edge(self.source, self.edge_target):
            edge = application.graph.edges[self.source, self.edge_target]
            self.old_status = edge.get("status", "ACTIVE")
            edge["status"] = "INACTIVE"
        self.active = True

    def revert(self, application):
        if self.old_status is not None and application.graph.has_edge(self.source, self.edge_target):
            application.graph.edges[self.source, self.edge_target]["status"] = self.old_status
        self.active = False
