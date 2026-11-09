from src.routing.network_loader import NetworkLoader
from src.routing.graph_builder import GraphBuilder
from src.routing.routing_engine import RoutingEngine


class Application:
    """Zentraler Zugriff auf die Fachlogik der Anwendung."""

    def __init__(self):
        network_data = NetworkLoader().load_network_data()

        self.graph = GraphBuilder().build(network_data)
        self.routing_engine = RoutingEngine(self.graph)

    def calculate_route(
        self,
        source: str,
        target: str,
    ) -> list[str]:
        return self.routing_engine.find_route(
            source,
            target,
        )

    def get_map_nodes(self):

        result = []

        for node_id, data in self.graph.nodes(data=True):

            result.append(
                {
                    "name": data["name"],
                    "lat": data["latitude"],
                    "lon": data["longitude"],
                    "typ": self._map_node_type(
                    data["node_type"]
                    )
                }
            )

        return result


    def _map_node_type(self, node_type):

        mapping = {

            "SUPPLIER":
            "LIEFERANT",

            "PORT":
            "HAFEN",

            "AIRPORT":
            "FLUGHAFEN",

            "FACTORY":
            "FABRIK",

            "WAREHOUSE":
            "LAGER",

            "RAIL_TERMINAL":
            "TERMINAL"
        }

        return mapping.get(
            node_type,
            "TERMINAL"
        )

    def get_nodes(self) -> list[dict]:
        """Liefert alle Knoten für die Weltkarte."""
        return [
            {
                "id": node_id,
                **attributes,
            }
            for node_id, attributes in self.graph.nodes(data=True)
        ]

    def get_edges(self) -> list[dict]:
        """Liefert alle Kanten für die Weltkarte."""
        return [
            {
                "source": source,
                "target": target,
                **attributes,
            }
            for source, target, attributes
            in self.graph.edges(data=True)
        ]

    def get_network_statistics(self) -> dict:
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
        }