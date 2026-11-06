import networkx as nx


class RoutingEngine:

    def __init__(
        self,
        graph
    ):

        self.graph = graph

    def find_route(
        self,
        source,
        target
    ):

        return nx.shortest_path(
            self.graph,
            source=source,
            target=target,
            weight="distance_km"
        )
