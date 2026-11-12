import networkx as nx


class RoutingEngine:
    WEIGHTS = {
        "FASTEST": "travel_time_h",
        "CHEAPEST": "cost",
        "LOWEST_CO2": "co2",
        "MOST_RESILIENT": "risk",
    }

    def __init__(self, graph):
        self.graph = graph

    def _active_graph(self):
        active_nodes = [
            node_id
            for node_id, data in self.graph.nodes(data=True)
            if data.get("status", "ACTIVE") == "ACTIVE"
        ]
        graph = self.graph.subgraph(active_nodes).copy()
        graph.remove_edges_from([
            (source, target)
            for source, target, data in graph.edges(data=True)
            if data.get("status", "ACTIVE") != "ACTIVE"
        ])
        return graph

    def calculate_route(self, source, target, strategy="FASTEST"):
        if strategy not in self.WEIGHTS:
            raise ValueError(f"Unbekannte Strategie: {strategy}")

        graph = self._active_graph()
        if source not in graph:
            raise nx.NodeNotFound(f"Startknoten ist nicht aktiv: {source}")
        if target not in graph:
            raise nx.NodeNotFound(f"Zielknoten ist nicht aktiv: {target}")

        weight = self.WEIGHTS[strategy]
        node_ids = nx.shortest_path(graph, source, target, weight=weight)
        segments = []
        totals = {"distance_km": 0.0, "cost": 0.0, "travel_time_h": 0.0, "co2": 0.0, "risk": 0.0}

        for start, end in zip(node_ids, node_ids[1:]):
            data = dict(graph.edges[start, end])
            segment = {"source": start, "target": end, **data}
            if not segment.get("geometry"):
                a, b = graph.nodes[start], graph.nodes[end]
                segment["geometry"] = [
                    [a["latitude"], a["longitude"]],
                    [b["latitude"], b["longitude"]],
                ]
            segments.append(segment)
            for key in totals:
                totals[key] += float(data.get(key, 0.0))

        return {
            "source": source,
            "target": target,
            "strategy": strategy,
            "node_ids": node_ids,
            "segments": segments,
            "total_distance_km": round(totals["distance_km"], 1),
            "total_cost": round(totals["cost"], 1),
            "total_time_h": round(totals["travel_time_h"], 1),
            "total_co2": round(totals["co2"], 1),
            "total_risk": round(totals["risk"], 2),
        }

    def find_route(self, source, target):
        return self.calculate_route(source, target, "FASTEST")["node_ids"]
