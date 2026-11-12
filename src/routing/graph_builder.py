import networkx as nx


class GraphBuilder:
    """Erstellt den gerichteten, gewichteten Multimodal-Graphen."""

    DEFAULT_RISK = {
        "TRUCK": 0.35,
        "RAIL": 0.18,
        "SHIP": 0.25,
        "AIR": 0.80,
        "BARGE": 0.20,
    }

    def build(self, network_data):
        graph = nx.DiGraph()

        all_nodes = []
        for key in (
            "suppliers",
            "ports",
            "airports",
            "rail_terminals",
            "factories",
            "warehouses",
            "bottlenecks",
        ):
            all_nodes.extend(network_data.get(key, []))

        for node in all_nodes:
            graph.add_node(node["id"], **node)

        modes = network_data["transport_modes"]
        geometries = network_data.get("geometries", {})

        for edge in network_data["edges"]:
            mode = edge["transport_mode"]
            profile = modes[mode]
            distance = float(edge["distance_km"])
            tonnes = float(edge.get("cargo_tonnes", 1.0))
            geometry_key = f'{edge["source"]}_{edge["target"]}'
            geometry = geometries.get(geometry_key, {})

            graph.add_edge(
                edge["source"],
                edge["target"],
                transport_mode=mode,
                ui_mode=geometry.get("ui_mode", self._ui_mode(mode)),
                geometry=geometry.get("geometry", []),
                distance_km=distance,
                travel_time_h=distance / float(profile["speed_kmh"]) + float(profile.get("terminal_hours", 0.0)),
                cost=distance * float(profile.get("cost_per_tkm", profile.get("cost_per_km", 0.0))),
                co2=distance * tonnes * float(profile["co2_per_tkm"]),
                risk=float(edge.get("risk", self.DEFAULT_RISK.get(mode, 0.5))),
                capacity=float(edge.get("capacity", 100.0)),
                status=edge.get("status", "ACTIVE"),
            )

        return graph

    @staticmethod
    def _ui_mode(mode):
        return {
            "TRUCK": "LKW",
            "RAIL": "ZUG",
            "SHIP": "SEESCHIFF",
            "AIR": "FLUGZEUG",
            "BARGE": "BINNENSCHIFF",
        }.get(mode, mode)
